#!/usr/bin/python3
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2018
import serial, re, time, sys, logging


logger = logging.getLogger(__name__)


msgfield = ['O2Concentration', 'AirSaturation', 'Temperature']
convf = [float, float, float]


def parse_3835(line):
    
    d = None
    line = line.strip()
    r = '.*MEASUREMENT\s+3835\s+(?P<SN>\d+)\s+' +\
          'Oxygen\:\s+(?P<O2Concentration>[+-]*\d+\.*\d*)\s+' +\
          'Saturation\:\s+(?P<AirSaturation>[+-]*\d+\.*\d*)\s+' +\
          'Temperature\:\s+(?P<Temperature>[+-]*\d+\.*\d*).*'
    r = re.match(r, line)
    if r is not None:
        d = {}
        for k, c in enumerate(msgfield):
            d[c] = convf[k](r.group(c))
    else:
        logger.debug('Format mismatch: {}'.format(line))
        print([ord(c) for c in line])
    return d


def aanderaa_3835_read(port, max_retry=5):
    logger.debug('aanderaa_3835_read()')
    
    with serial.Serial(port, 9600, timeout=2) as ser:
        
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
                    try:
                        r = parse_3835(line)
                        if r:
                            break
                    except ValueError:
                        logger.debug('(valueerror)')

            except UnicodeDecodeError:
                logger.exception('UnicodeDecodeError: {}'.format(line))
                ser.flush()

            time.sleep(1)

        ser.flush()
        return r


if '__main__' == __name__:
    
    #c1 = 'MEASUREMENT	  3835	   506	Oxygen: 	   264.81	Saturation: 	    90.54	Temperature: 	    18.47'
    #c2 = 'MEASUREMENT	  3835	   505	Oxygen: 	   287.81	Saturation: 	    95.10	Temperature: 	    16.82'
    #c3 = 'only nixon can go to china'
    #print parse_3835(c1)
    #print parse_3835(c2)
    #print parse_3835(c3)

    logger.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)

    DEFAULT_PORT = '/dev/ttyS1'
    PORT = input('PORT=? (default={})'.format(DEFAULT_PORT)).strip()
    if len(PORT) <= 0:
        PORT = DEFAULT_PORT

    while True:
        try:
            print(aanderaa_3835_read(PORT))
        except KeyboardInterrupt:
            print('user interrupted')
            break
