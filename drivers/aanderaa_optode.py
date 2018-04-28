import logging, time, sys
from serial import Serial
from . import aanderaa_3835
from . import aanderaa_4330f
from . import aanderaa_4531d


logger = logging.getLogger(__name__)


def optode_read_universal(port, max_retry=5, parsers=[aanderaa_4531d.parse_4531d, aanderaa_4330f.parse_4330f, aanderaa_3835.parse_3835]):
    logger.debug('optode_read_universal()')
    
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

                if any([c in line for c in '#*']):
                    logger.debug('(junk)')
                    logger.debug(line)
                    logger.debug([ord(c) for c in line])
                    continue
                elif len(line) <= 0:
                    logger.debug('(no response)') 
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
                            if r:
                                break
                        except ValueError:
                            logger.debug('(valueerror)')

            except UnicodeDecodeError:
                logger.exception('UnicodeDecodeError: {}'.format(line))
                ser.flush()

            if r is not None:
                break

            time.sleep(1)

        ser.flush()
        return r


if '__main__' == __name__:

    logger.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)

    DEFAULT_PORT = '/dev/ttyS1'
    PORT = input('PORT=? (default={})'.format(DEFAULT_PORT)).strip()
    if len(PORT) <= 0:
        PORT = DEFAULT_PORT

    while True:
        try:
            print(optode_read_universal(PORT))
        except KeyboardInterrupt:
            print('user interrupted')
            break
