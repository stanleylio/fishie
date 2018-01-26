# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2018
# University of Hawaii
import serial, logging, time

logger = logging.getLogger(__name__)


def parse_4319a(line):
    tmp = line.strip().replace('\x11','').replace('\x13','').split('\t')
    
    if '4319' not in tmp[0]:
        logger.debug('4319 tag not found')
        logger.debug(line)
        return None
    if len(tmp) != 4:
        logger.debug('Expected 4 fields')
        logger.debug(line)
        return None
    line = tmp
    tags = ['sn','ec','t']
    line[2] = float(line[2])
    line[3] = float(line[3])
    return dict(zip(tags, line[1:]))

def aanderaa_4319a_read(port):
    """return specific conductivity in mS/cm"""
    with serial.Serial(port, 9600, timeout=2) as s:
        retry = 3
        r = None
        for i in range(retry):
            s.write('\r\ndo sample\r\n'.encode())
            line = s.readline().decode().strip()
            if '#' in line or len(line) <= 0:
                continue
            try:
                r = parse_4319a(line)
                if r:
                    break
            except ValueError:
                pass
            time.sleep(0.5)
        return r


if '__main__' == __name__:
    
    logging.basicConfig(level=logging.DEBUG)
    
    while True:
        try:
            print(aanderaa_4319a_read('/dev/ttyS0'))
        except ValueError:
            pass
