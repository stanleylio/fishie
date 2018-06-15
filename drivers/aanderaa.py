# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2018
import logging, time, sys
from serial import Serial
from . import aanderaa_3835
from . import aanderaa_4330f
from . import aanderaa_4531d
from . import aanderaa_4319a


logger = logging.getLogger(__name__)


# works with 3835 (DO), 4330F (DO), 4531D (DO), and 4319A (EC)
def aanderaa_read_universal(port, max_retry=3, parsers=[aanderaa_4531d.parse_4531d, aanderaa_4330f.parse_4330f, aanderaa_3835.parse_3835, aanderaa_4319a.parse_4319a]):
    logger.debug('aanderaa_read_universal()')
    
    with Serial(port, 9600, timeout=2) as ser:

        r = None
        for _ in range(max_retry):

            ser.flush()
            ser.write(b'\r\ndo sample\r\n')
            try:
                line = ser.readline()
                line = filter(lambda c: c <= 0x7f, line)
                line = bytearray(filter(lambda c: c not in ['\x11', '\x13'], line))    # the control characters
                line = line.decode().strip()
                #print([ord(c) for c in line])

                if len(line) <= 0:
                    logger.debug('(no response)') 
                    continue
                elif any([c in line for c in '#*']):
                    logger.debug('(junk)')
                    logger.debug(line)
                    logger.debug([ord(c) for c in line])
                    continue
                elif 'SYNTAX ERROR' in line:
                    logger.debug('(SYNTAX ERROR)')
                    logger.debug([ord(c) for c in line])
                    continue
                else:
                    for f in parsers:
                        logging.debug(f)
                        try:
                            r = f(line)
                            if r is not None and len(r) > 0:
                                break
                        except ValueError:
                            logger.debug('(valueerror)')
                    else:
                        time.sleep(1.29)
                        ser.flush()

            except UnicodeDecodeError:
                logger.exception('UnicodeDecodeError: {}'.format(line))
                ser.flush()

            if r is not None and len(r.keys()):
                break

            time.sleep(1.17)

        ser.flush()
        return r


if '__main__' == __name__:

    logger.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO)

    DEFAULT_PORT = '/dev/ttyS1'
    PORT = input('PORT=? (default={})'.format(DEFAULT_PORT)).strip()
    if len(PORT) <= 0:
        PORT = DEFAULT_PORT

    while True:
        try:
            print(aanderaa_read_universal(PORT))
        except KeyboardInterrupt:
            print('user interrupted')
            break
