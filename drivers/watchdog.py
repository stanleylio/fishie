#!/usr/bin/python
#
# Stanley Hou In Lio, hlio@hawaii.edu
# October 1, 2015
import sys,time,os,traceback
from Adafruit_GPIO.I2C import Device


class Watchdog(object):
    def __init__(self,addr=0x51,bus=1):
        self._i2c = Device(addr,busnum=bus)

    def reset(self):
        return self._i2c.readU16(10)


if '__main__' == __name__:
    for bus in [1,2]:
        try:
            w = Watchdog(bus=bus)
            for i in range(10):
                w.reset()
            print('Found watchdog on bus {}'.format(bus))
        except:
            #print('nope.')
            #traceback.print_exc()
            pass

