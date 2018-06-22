from time import sleep
from smbus import SMBus
import traceback


class Si1145:
    address = 0x60

    # I2C register addresses (P.29)
    PARAM_WR = 0x17
    COMMAND = 0x18
    RESPONSE = 0x20
    PARAM_RD = 0x2E

    # RAM addresses (P.45)
    CHLIST = 0x01
    ALS_IR_ADCMUX = 0x0E
    ALS_IR_ADC_GAIN = 0x1E
    ALS_IR_ADC_MISC = 0x1F
    ALS_VIS_ADC_GAIN = 0x11
    ALS_VIS_ADC_MISC = 0x12
    
    def __init__(self,bus=1):
        self.bus = SMBus(bus)
        self.reset()
        sleep(0.005)    # > 1ms
        self._write(0x07,self.PARAM_WR)
        self.enable()

    def check_ID(self):
        return 0x45 == self._read(0)

    def read_raw(self):
        try:
            self._write(self.COMMAND,0)
            if not 0 == self._read(self.RESPONSE):
                print('what\s the point of a check if you\'re not doing anything about it...')
                return
            self._write(self.COMMAND,0b00000110)    # P.23 ALS_FORCE
            sleep(0.0005)
            r = {}
            r['visible'] = self.bus.read_word_data(self.address,0x22)
            r['ir'] = self.bus.read_word_data(self.address,0x24)
            r['uv'] = self.bus.read_word_data(self.address,0x2C)
            return r
        except IOError:
            traceback.print_exc()
            #pass
        return None

    def read(self):
        try:
            r = self.read_raw()
            r['visible'] = round(r['visible']/0.282,2)  # P.6
            r['ir'] = round(r['ir']/2.44,2) # P.7; assume small IR photodiode
            r['uv'] = round(r['uv']/100.,1)
            return r
        except TypeError:
            traceback.print_exc()
            #pass
        except:
            pass
            #raise
        return None

    def reset(self):
        self._write(self.COMMAND,0)
        if not 0 == self._read(self.RESPONSE):
            print('Si1145::reset() failed')
            return
        self._write(self.COMMAND,1) # P.22 Table 5

    def high_signal_range(self):
        self.set_param(self.ALS_IR_ADCMUX,0)    # P.55 (small IR photodiode)
        #self.set_param(self.ALS_IR_ADCMUX,3)    # P.55 (large IR photodiode)
        self.set_param(self.ALS_IR_ADC_GAIN,0)  # P.59 (/1)
        #self.set_param(self.ALS_IR_ADC_GAIN,4)  # P.59 (/16)
        #self.set_param(self.ALS_IR_ADC_GAIN,6)  # P.59 (/64)
        tmp = self.query_param(self.ALS_IR_ADC_MISC)    # P.59 read-modify-write as required
        self.set_param(self.ALS_IR_ADC_MISC,tmp | 0b00100000)     # P.59 High Signal Range (gain/14.5)

        self.set_param(self.ALS_VIS_ADC_GAIN,0) # P.57 (/1)
        #self.set_param(self.ALS_VIS_ADC_GAIN,4) # P.57 (/16)
        #self.set_param(self.ALS_VIS_ADC_GAIN,6) # P.57 (/64)
        self.set_param(self.ALS_VIS_ADC_MISC,0b00100000)    # P.57 High Signal Range (gain/14.5)

    def enable(self):
        self._write(0x13,0x7B)  # P.16 UV stuff
        self._write(0x14,0x6B)
        self._write(0x15,1)
        self._write(0x16,0)
        return self.set_param(self.CHLIST,0b11110000)   # P.47

    def query_param(self,param):
        """Read a RAM parameter
        param: RAM address of the parameter"""
        self._write(self.COMMAND,0)
        if not 0 == self._read(self.RESPONSE):
            print('Si1145::query_param() failed')
            return
        self._write(self.COMMAND,0x80 | param)  # PARAM_QUERY, P.22
        for i in range(10):
            if not 0 == self._read(self.RESPONSE):
                return self._read(self.PARAM_RD)
        return

    def set_param(self,param,val):
        """Set a RAM parameter
        param: RAM address of the parameter
        val: value to be written"""
        self._write(self.PARAM_WR,val)  # put val in "mailbox" register PARAM_WR
        self._write(self.COMMAND,0)
        if not 0 == self._read(self.RESPONSE):
            print('Si1145::set_param() failed')
            return
        self._write(self.COMMAND,0xA0 | param)  # PARAM_SET, P.22
        for i in range(10):
            if not 0 == self._read(self.RESPONSE):
                return self._read(self.PARAM_RD)
        return

    def _read(self,reg):
        return self.bus.read_byte_data(self.address,reg)

    def _write(self,r,v):
        self.bus.write_byte_data(self.address,r,v)


if '__main__' == __name__:
    s = Si1145(bus=1)
    assert s.check_ID()
    #print bin(s.query_param(s.CHLIST))

    #s.high_signal_range()
    
    while True:
        try:
            print(s.read())
            sleep(0.1)
        except IOError:
            pass
        except KeyboardInterrupt:
            print('user interrupted')
            break

