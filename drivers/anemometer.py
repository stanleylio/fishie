#!/usr/bin/python
import sys,time
sys.path.append('Adafruit_GPIO')
from I2C import Device

class Anemometer(object):
    def __init__(self,addr=0x50):
        self._i2c = Device(addr,busnum=1)

    def read(self):
        speed_reg = 10
        gust_reg = 11
        
        S = []
        for i in range(100):
            v = self._i2c.readU16(speed_reg)
            S.append(v)
            time.sleep(0.001)

        if len(S) > 0:
            v = sum(S)/len(S)
            v = self.conv(v)
        else:
            v = None

        g = self._i2c.readU16(gust_reg)
        g = self.conv(g)
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
        #print '{:.2f} m/s'.format(a.read())
        print '{},{:.2f},{:.2f}'.format(time.time(),r['speed'],r['gust'])
        #time.sleep(1)
