#!/usr/bin/python3
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2018
import serial, re, time, sys, logging


logger = logging.getLogger(__name__)


msgfield = ['O2Concentration', 'AirSaturation', 'Temperature']
convf = [float, float, float]


def parse_4531(line):
    
    d = None
    line = line.strip()
    r = '.*MEASUREMENT\s+4531\s+(?P<SN>\d+)\s+' +\
          'O2Concentration\[uM\]\s+(?P<O2Concentration>[+-]*\d+\.*\d*)\s+' +\
          'AirSaturation\[%\]\s+(?P<AirSaturation>[+-]*\d+\.*\d*)\s+' +\
          'Temperature\[Deg\.C\]\s+(?P<Temperature>[+-]*\d+\.*\d*).*'
    r = re.match(r, line)
    if r is not None:
        d = {}
        for k, c in enumerate(msgfield):
            d[c] = convf[k](r.group(c))
    else:
        logger.debug('Format mismatch: {}'.format(line))
        print([ord(c) for c in line])
    return d


def aanderaa_4531_read(port, max_retry=5):
    logger.debug('aanderaa_4531_read()')
    
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
                        r = parse_4531(line)
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

    '''MEASUREMENT	4531	395	O2Concentration[uM]	259.160	AirSaturation[%]	97.999	Temperature[Deg.C]	23.662
MEASUREMENT	4531	395	O2Concentration[uM]	259.050	AirSaturation[%]	97.957	Temperature[Deg.C]	23.662
MEASUREMENT	4531	395	O2Concentration[uM]	258.975	AirSaturation[%]	97.928	Temperature[Deg.C]	23.661
MEASUREMENT	4531	395	O2Concentration[uM]	259.072	AirSaturation[%]	97.956	Temperature[Deg.C]	23.657
MEASUREMENT	4531	395	O2Concentration[uM]	259.197	AirSaturation[%]	97.994	Temperature[Deg.C]	23.652
MEASUREMENT	4531	395	O2Concentration[uM]	259.092	AirSaturation[%]	97.947	Temperature[Deg.C]	23.648
MEASUREMENT	4531	395	O2Concentration[uM]	258.967	AirSaturation[%]	97.899	Temperature[Deg.C]	23.647
'''
    
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)

    DEFAULT_PORT = '/dev/ttyS1'
    PORT = input('PORT=? (default={})'.format(DEFAULT_PORT)).strip()
    if len(PORT) <= 0:
        PORT = DEFAULT_PORT

    while True:
        try:
            print(aanderaa_4531_read(PORT))
        except KeyboardInterrupt:
            print('user interrupted')
            break
