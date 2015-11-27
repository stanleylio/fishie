#!/usr/bin/python
#
# Stanley Hou In Lio, hlio@hawaii.edu
# November 26, 2015
import serial,time,traceback


class Anemometer(object):
    max_speed = 32.4
    
    def __init__(self,port):
        self._port = port
        self._baud = 9600

    def read(self):
        return {'raw':self.raw(),'speed':self.average(),'gust':self.gust()}

    # raw ADC reading (10-bit res)
    def raw(self):
        return self._get(cmd='r')

    def average(self):
        return round(Anemometer.conv(self._get(cmd='a'))*10)/10.

    def gust(self):
        return round(Anemometer.conv(self._get(cmd='g'))*10)/10.

    def _get(self,cmd):
        count = 0
        line = ''
        with serial.Serial(self._port,9600,timeout=0.3) as s:
            s.flushInput()
            while len(line) <= 0 and count < 5:
                s.write(cmd)
                s.flushOutput()
                line = s.readline()
            try:
                return int(line)
            except:
                traceback.print_exc()
                return None

    @staticmethod
    def conv(v):
        #s = v/255.0*2.56   # LUFA RingBuffer doesn't take uint16_t
        #s = v/1023.0*2.56  # Pro Micro's 2.56V ref is perfect
        s = v/1023.0*3.3    # Pro Mini either use 1.1V or Vcc as ref
        return 32.4/1.6*(s - 0.4)


if '__main__' == __name__:

    a = Anemometer(port='COM11')

    '''while True:
        time.sleep(0.1)
        try:
            print a.average(),a.gust(),a.raw()
        except KeyboardInterrupt:
            break
        except:
            traceback.print_exc()'''

    while True:
        #time.sleep(1)
        try:
            r = a.read()

            #print('\x1b[2J\x1b[;H')
            print('Raw ADC reg={}\t\tAverage={:.1f}m/s\t\tGust={:.1f}m/s\t'.\
                  format(r['raw'],r['speed'],r['gust']))
            #print a.average()
            #print a.raw()
            #print a.duh()
        except KeyboardInterrupt:
            break
        except IOError:
            traceback.print_exc()
        except:
            traceback.print_exc()

