import binascii, logging
from serial import Serial


logger = logging.getLogger(__name__)

class RMY05106:
    def __init__(self, port, *_, baud=115200, serialtimeout=0.1):
        self._s = Serial(port, baud, timeout=serialtimeout)

    def __del__(self):
        try:
            self._s.close()
        except:
            pass

    def read(self):
        for i in range(5):
            #self._s.flushOutput()
            #self._s.flushInput()
            self._s.write(b'RMY05106,rfd\r\n')
            bline = self._s.readline()
            try:
                line = bline.decode()
                if line.startswith('RMY05106,rfd,'):
                    r = line.strip().split(',')
                    crc = binascii.crc32(bline[0:line.rfind(',')]) & 0xffffffff
                    if '%08x' % crc == r[-1]:
                        v = {}
                        v['v'] = round(float(r[2])*0.098, 2)
                        v['d'] = round(float(r[3])*360.0, 1)%360
                        return v
            except:
                logger.exception('rmy')


if '__main__' == __name__:
    import time

    logging.basicConfig(level=logging.DEBUG)
    
    rmy = RMY05106('/dev/ttyS0', baud=9600, serialtimeout=1)
    while True:
        print(rmy.read())
        time.sleep(0.1)
