from __future__ import division
from smbus import SMBus
import traceback,time


class Si7051(object):
    address = 0x40

    TEMP_HOLD = 0xE3
    #TEMP_NOHOLD = 0xF3
    #RESET = 0xFE
    #W_USER_REG = 0xE6
    #R_USER_REG = 0xE7
    #R_ID1 = 0xFA0F
    #R_ID2 = 0xFCC9
    #R_FIRMWARE_REV = 0x84B8

    def __init__(self,bus=1):
        self.bus = SMBus(bus)

    def read(self):
        # http://wiki.erazor-zone.de/wiki:linux:python:smbus:doc
        # default 14-bit
        tmp = self.bus.read_i2c_block_data(self.address,self.TEMP_HOLD)
        tmp = (tmp[0] << 8) + tmp[1]
        return round(175.72*tmp/65536 - 46.85,6)


if '__main__' == __name__:
    s = Si7051(bus=2)
    while True:
        print(s.read())
        time.sleep(0.2)
