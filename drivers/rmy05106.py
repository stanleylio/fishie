import binascii
from serial import Serial


class RMY05106:
    def __init__(self,port,baud=115200):
        self._s = Serial(port,baud,timeout=0.1)

    def __del__(self):
        try:
            self._s.close()
        except:
            pass

    def read(self):
        for i in range(3):
            self._s.flushOutput()
            self._s.flushInput()
            self._s.write('RMY05106,rfd\r\n')
            line = self._s.readline()
            try:
                if line.startswith('RMY05106,rfd,'):
                    r = line.strip().split(',')
                    crc = binascii.crc32(line[0:line.rfind(',')]) & 0xffffffff
                    if '%08x' % crc == r[-1]:
                        v = {}
                        v['v'] = round(float(r[2])*0.098,2)
                        v['d'] = round(float(r[3])*360.0,1)%360
                        return v
            except:
                #traceback.print_exc()
                pass


if '__main__' == __name__:
    import time
    
    rmy = RMY05106('/dev/ttyS0')
    while True:
        print(rmy.read())
        time.sleep(0.1)
