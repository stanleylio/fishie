#!/usr/bin/python
#
# Stanley Hou In Lio, hlio@hawaii.edu
# October 1, 2015
import sys,time,os,traceback
sys.path.append(os.path.join(os.path.dirname(__file__),'Adafruit_GPIO'))
from I2C import Device
from scipy.signal import medfilt


class Anemometer(object):
    max_speed = 32.4
    speed_reg = 10
    gust_reg = 11
    raw_reg = 12
    
    def __init__(self,addr=0x50,bus=1):
        self._i2c = Device(addr,busnum=bus)

    def read(self):
        return {'raw':self.raw(),'speed':self.average(),'gust':self.gust()}

    # raw ADC reading (16-bit)
    def raw(self):
        return self._i2c.readU16(self.raw_reg)

    # average wind speed (8-bit resolution due to LUFA RingBuffer limit)
    # this takes one minute to stabilize
    def average(self):
        for i in range(10):
            try:
                v = self.conv(self._i2c.readU16(self.speed_reg))
                break
            except IOError:
                pass
        return max(round(v*10)/10.,0)

    # wind gust (8-bit resolution due to LUFA RingBuffer limit)
    def gust(self):
        for i in range(10):
            try:
                v = self.conv(self._i2c.readU16(self.gust_reg))
                break
            except IOError:
                pass
        return round(v*10)/10.

    #def duh(self):
    #    return self._i2c.readU16(self.speed_reg)

    @staticmethod
    def conv(v):
        #s = v/255.0*2.56;     # LUFA RingBuffer doesn't take uint16_t
        s = v/1023.0*2.56;
        return 32.4/1.6*(s - 0.4);


if '__main__' == __name__:

    a = Anemometer()

    while True:
        try:
            r = a.read()

            #print('\x1b[2J\x1b[;H')
            print('Raw ADC reg={}\t\tAverage={:.1f}m/s\t\tGust={:.1f}m/s\t'.\
                  format(r['raw'],r['speed'],r['gust']))
            #print a.average()
            #print a.raw()
            #print a.duh()
            time.sleep(1)
        except KeyboardInterrupt:
            break
        except IOError:
            pass
        except:
            traceback.print_exc()

