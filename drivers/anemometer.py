#!/usr/bin/python
#
# Stanley Hou In Lio, hlio@hawaii.edu
# October 1, 2015
import sys,time,os
sys.path.append(os.path.join(os.path.dirname(__file__),'Adafruit_GPIO'))
from I2C import Device
from scipy.signal import medfilt


class Anemometer(object):
    max_speed = 32.4
    
    def __init__(self,addr=0x50):
        self._i2c = Device(addr,busnum=1)

    def read(self):
        speed_reg = 10
        gust_reg = 11

        for i in range(5):
            v = self.conv(self._i2c.readU16(speed_reg))
            if v >= 0 and v <= self.max_speed:
                v = round(v*100)/100
                break
        if v < 0 or v > self.max_speed:
            v = None

        for i in range(5):
            g = self.conv(self._i2c.readU16(gust_reg))
            if g >= 0 and g <= self.max_speed:
                g = round(g*100)/100
                break
        if g < 0 or g > self.max_speed:
            g = None
        
        return {'speed':v,'gust':g}

    @staticmethod
    def conv(v):
        s = v/1023.0*2.56;
        s = 32.4/1.6*(s - 0.4);
        return s


if '__main__' == __name__:

    a = Anemometer()

    while True:
        r = a.read()
        if r['speed'] is not None and r['gust'] is not None:
            print('\x1b[2J\x1b[;H')
            print('Speed={:.2f}m/s\tGust={:.2f}m/s\t'.format(r['speed'],r['gust']))
            #print '{},{:.2f},{:.2f}'.format(time.time(),r['speed'],r['gust'])
            time.sleep(5)

