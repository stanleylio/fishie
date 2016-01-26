# Driver for 20x4 LCD via PCF8574T
# Tested on Beaglebone Black + Debian
#
# Stanley Lio, hlio@hawaii.edu
# January 2016
import time
from smbus import SMBus

# P0(4) RS(4)
# P1(5) R/W(5)
# P2(6) E(6)
# P3
# P4(9) DB4(11)
# P5(10) DB5(12)
# P6(11) DB6(13)
# P7(12) DB7(14)

class LCD(object):
    PCF8574T_addr = 0x27
    RS = 0
    RW = 1
    E = 2
    BL = 3
    DB4 = 4
    DB5 = 5
    DB6 = 6
    DB7 = 7
    
    def __init__(self,bus=1):
        self._bus = SMBus(bus)
        self._state = 0

        self.backlight(True)

        self.clear_RW()    # write
        self.clear_RS()    # instruction

        # 4-bit mode
        self.set_E()
        self.setbit(self.DB5)
        self.setbit(self.DB4)
        time.sleep(0.001)
        self.clear_E()
        time.sleep(0.01)
        self.set_E()
        self.setbit(self.DB5)
        self.setbit(self.DB4)
        time.sleep(0.001)
        self.clear_E()
        time.sleep(0.01)
        self.set_E()
        self.setbit(self.DB5)
        self.setbit(self.DB4)
        time.sleep(0.001)
        self.clear_E()
        time.sleep(0.01)
        self.set_E()
        self.setbit(self.DB5)
        self.clearbit(self.DB4)
        time.sleep(0.001)
        self.clear_E()
        time.sleep(0.01)

        # 4-bit mode, continue
        self.sendbyte(0b00101000)
        time.sleep(0.005)

        self.clear()
        self.home()

        # cursor direction... the default is good.
        #self.sendbyte(0b00000111)
        # turn ON display; turn OFF cursor and blink
        self.sendbyte(0b00001100)

    def write_lines(self,lines):
        while len(lines) < 4:
            lines.append([])
        for line in [lines[k] for k in (0,2,1,3)]:
            self.write_str(line)
            if len(line) < 20:
                self.write_str(' '*(20 - len(line)))

    def write_str(self,s):
        for c in s:
            self.write_char(c)

    def write_char(self,c):
        self.set_RS()
        self.sendbyte(ord(c))

    def clear(self):
        self.clear_RS()
        self.sendbyte(1)
        #self.set_RS()
        time.sleep(0.005)

    def home(self):
        self.clear_RS()
        self.sendbyte(2)
        #self.set_RS()
        time.sleep(0.005)

    def sendbyte(self,byte):
        #print bin(self._state)
        self.set_E()
        self._state = (byte & 0xF0) | (self._state & 0x0F)
        self._bus.write_byte(self.PCF8574T_addr,self._state)
        self.clear_E()

        self.set_E()
        self._state = (self._state & 0x0F) | ((byte & 0x0F) << 4)
        self._bus.write_byte(self.PCF8574T_addr,self._state)
        self.clear_E()
        
    #def writebyte(self,byte):
        #self._bus.write_byte(self.PCF8574T_addr,byte)
        # don't do this - it changes the other nibble as well

    def backlight(self,b):
        if b:
            self.setbit(self.BL)
        else:
            self.clearbit(self.BL)

    def setbit(self,bit):
        self._state = self._state | 1 << bit
        self._bus.write_byte(self.PCF8574T_addr,self._state)

    def clearbit(self,bit):
        self._state = self._state & (255 - (1 << bit))
        self._bus.write_byte(self.PCF8574T_addr,self._state)
        
    def set_RS(self):
        self.setbit(self.RS)

    def clear_RS(self):
        self.clearbit(self.RS)

    def set_RW(self):
        self.setbit(self.RW)

    def clear_RW(self):
        self.clearbit(self.RW)

    def set_E(self):
        self.setbit(self.E)

    def clear_E(self):
        self.clearbit(self.E)

    
if '__main__' == __name__:
    d = LCD(bus=2)
    d.write_lines(['John C Calhoun','RioT!!','Mary Seacole','PARTY HARD!!!'])

    while True:
        d.backlight(True)
        time.sleep(0.1)
        d.backlight(False)
        time.sleep(0.1)
    

