"""Driver for TCS34725 RGB light sensor
Stanley Lio, hlio@soest.hawaii.edu
All Rights Reserved. February 2016
"""
from time import sleep
from smbus import SMBus


def PRINT(s):
    pass
    #print(s)

class DeviceNotFoundException(Exception):
    pass

class TCS34725(object):
    address = 0x29

    AGAIN = [0,1,2,3]
    GAIN = [1,4,16,60]

    INT_TIME = [2.4,24,101,154,700]     # ms

    # The middle one should be 0xd6 for the table to be correct... unless, of course,
    # the other two were wrong and 0xD5 is correct.
    ATIME = [0xff,0xf6,0xd6,0xc0,0x00]
    
    def __init__(self,bus=1,gain=0,integration_time=0xff):
        self.bus = SMBus(bus)
        if not self.check_ID():
            # it'd be nice to have the drivers locate the sensor on the buses, but then
            #   RPi has only one I2C bus, and
            #   what if I have the same type of sensor on both buses?
            raise DeviceNotFoundException('TCS34725 not found on bus {}'.format(bus))
        self.gain(gain)
        self.integration_time(integration_time)
        self.enable()

    def check_ID(self):
        return 0x44 == self._read(0x12)

    def enable(self):
        """see notes on P.15"""
        self._write(0,0b1)
        sleep(0.003)
        self._write(0,0b11)

    def disable(self):
        self._write(0,0)
        
    def status(self):
        return self._read(0x13)

    def readCRGB(self):
        r = self.bus.read_i2c_block_data(self.address,0x80 + 0x14,8)
        mc = min((256 - self._it)*1024,65535)
        r = {'c':float((r[1] << 8) + r[0])/mc,
             'r':float((r[3] << 8) + r[2])/mc,
             'g':float((r[5] << 8) + r[4])/mc,
             'b':float((r[7] << 8) + r[6])/mc,}
        return r

    def integration_time(self,it=None):
        if it is not None:
            if it not in self.ATIME:
                raise AttributeError('integration time must be one of {} (corresponding to {}ms)'.format(self.ATIME,self.INT_TIME))
            self._write(0x01,it)
        tmp = self._read(0x01)
        self._it = tmp
        return tmp

    def gain(self,gain=None):
        if gain is not None:
            if gain not in self.AGAIN:
                raise AttributeError('gain must be one of {} (corresponding to one of {}x)'.format(self.AGAIN,self.GAIN))
            self._write(0x0f,gain)
        tmp = self._read(0x0f)
        self._gain = tmp
        return tmp
    
    #def duh(self):
    #    print [self._read(0x00),self._read(0x01),self._read(0x0f)]

    def _read(self,reg):
        # so this would be a so-called "combined protocol"
        return self.bus.read_byte_data(self.address,0x80 + reg)
        
    def _write(self,reg,value):
        self.bus.write_byte_data(self.address,0x80 + reg,value)

    def __del__(self):
        #self.disable()
        pass


if '__main__' == __name__:
    s = TCS34725(bus=2)
    s.gain(TCS34725.AGAIN[0])
    s.integration_time(TCS34725.ATIME[0])

    #s.duh()
    #print s.gain()
    #print s.integration_time()

    while True:
        r = s.readCRGB()
        print ''.join(['c']*int(round(r['c']*10))) + ' ' + '{:.3f}'.format(r['c'])
        sleep(0.1)
    
