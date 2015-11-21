#!/usr/bin/python
#
# Stanley Hou In Lio, hlio@hawaii.edu
# October 1, 2015
import sys,time,os
#sys.path.append(os.path.join(os.path.dirname(__file__),'Adafruit_GPIO'))
import Adafruit_GPIO
from Adafruit_GPIO.I2C import Device
from scipy.signal import medfilt


class Watchdog(object):
    def __init__(self,addr=0x51,bus=1):
        self._i2c = Device(addr,busnum=bus)

    def reset(self):
        tmp = self._i2c.readU16(10)


if '__main__' == __name__:
    for bus in [1,2]:
        try:
            w = Watchdog(bus=bus)
            for i in range(10):
                w.reset()
            print('found watchdog on bus {}'.format(bus))
        except:
            #print('nope.')
            pass
