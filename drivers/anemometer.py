#!/usr/bin/python
#
# Stanley Hou In Lio, hlio@hawaii.edu
# October 1, 2015
import sys,time,os
sys.path.append(os.path.join(os.path.dirname(__file__),'Adafruit_GPIO'))
from I2C import Device
from scipy.signal import medfilt

class Anemometer(object):
    def __init__(self,addr=0x50):
        self._i2c = Device(addr,busnum=1)

    def read(self):
        speed_reg = 10
        gust_reg = 11
        
        S = []
        for i in range(100):
            # These kinds of low-level calls never "fail" - only the
            # application tell whether the return values make sense
            # or not.
            v = self._i2c.readU16(speed_reg)
            S.append(v)
            time.sleep(0.001)

        if len(S) > 0:
            # A cheap way to get rid of the failed values is the
            # median filter.
            S = medfilt(S,7)
            v = sum(S)/len(S)
            v = self.conv(v)

            # What does "negative wind speed" even mean?
            # happens when the anemometer lose power. "0m/s" is at 0.4V.
            v = max([v,0])
        else:
            v = None

        g = self._i2c.readU16(gust_reg)
        g = self.conv(g)
        g = max([g,0])  # see v above.
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
        #print("\x1b[2J\x1b[;H")
        #print '{:.2f} m/s'.format(a.read())
        print '{},{:.2f},{:.2f}'.format(time.time(),r['speed'],r['gust'])
        #time.sleep(1)
