# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2018
import re, logging


logger = logging.getLogger(__name__)


def parse_3835(line):
    msgfield = ['SN', 'O2Concentration', 'AirSaturation', 'Temperature']
    convf = [int, float, float, float]
    convf = dict(zip(msgfield, convf))
    
    d = None
    line = line.strip()
    r = '.*MEASUREMENT\s+3835\s+(?P<SN>\d+)\s+' +\
          'Oxygen\:\s+(?P<O2Concentration>[+-]*\d+\.*\d*)\s+' +\
          'Saturation\:\s+(?P<AirSaturation>[+-]*\d+\.*\d*)\s+' +\
          'Temperature\:\s+(?P<Temperature>[+-]*\d+\.*\d*).*'
    r = re.match(r, line)
    if r:
        return {k:convf[k](v) for k,v in r.groupdict().items()}
    else:
        logger.debug('Format mismatch: {}'.format(line))
        logger.debug([ord(c) for c in line])
    return d


def aanderaa_3835_read(port, max_retry=5):
    from . import aanderaa
    return aanderaa.aanderaa_read_universal(port, max_retry=max_retry, parsers=[parse_3835])


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
