# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2018
# University of Hawaii
import re, logging


logger = logging.getLogger(__name__)


def parse_4319a(line):
    msgfield = ['SN', 'Conductivity', 'Temperature', 'Salinity', 'Density', 'Soundspeed']
    convf = [int, float, float, float, float, float]
    convf = dict(zip(msgfield, convf))

    d = None
    line = line.strip()

    # Text disabled (measured only, no derived parameters)
    p1 = '.*4319\s+(?P<SN>\d+)\s+(?P<Conductivity>[+-]?\d+\.*\d*)\s+(?P<Temperature>[+-]?\d+\.*\d*)\s+'

    # Text enabled (measured only, no derived parameters)
    p2 = '.*MEASUREMENT\s+4319\s+(?P<SN>\d+)\s+' +\
          'Conductivity\[mS/cm\]\s+(?P<Conductivity>[+-]?\d+\.*\d*)\s+' +\
          'Temperature\[Deg\.C\]\s+(?P<Temperature>[+-]?\d+\.*\d*).*'

    # Text enabled (with derived parameters)
    p3 = '.*MEASUREMENT\s+4319\s+(?P<SN>\d+)\s+' +\
          'Conductivity\[mS/cm\]\s+(?P<Conductivity>[+-]?\d+\.*\d*)\s+' +\
          'Temperature\[Deg\.C\]\s+(?P<Temperature>[+-]?\d+\.*\d*).*' +\
          'Salinity\[PSU\]\s+(?P<Salinity>[+-]?\d+\.*\d*).*' +\
          'Density\[kg/m3\]\s+(?P<Density>[+-]?\d+\.*\d*).*' +\
          'Soundspeed\[m/s\]\s+(?P<Soundspeed>[+-]?\d+\.*\d*).*'

    for p in [p3, p2, p1]:
        r = re.match(p, line)
        if r:
            return {k:convf[k](v) for k,v in r.groupdict().items()}
    else:
        logger.debug('Format mismatch: {}'.format(line))
        logger.debug([ord(c) for c in line])
        #open('/home/nuc/wtf.txt', 'a').write(line)
    return {}


def aanderaa_4319a_read(port, max_retry=5):
    from . import aanderaa
    return aanderaa.aanderaa_read_universal(port, max_retry=max_retry, parsers=[parse_4319a])


if '__main__' == __name__:

    #print(parse_4319a(' MEASUREMENT  4319    1412    Conductivity[mS/cm]     -0.007  Temperature[Deg.C]      22.654  Salinity[PSU]   0.013   Density[kg/m3]  997.632 Soundspeed[m/s] 1490.236'))
    #exit()
    
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)

    DEFAULT_PORT = '/dev/ttyS1'
    PORT = input('PORT=? (default={})'.format(DEFAULT_PORT)).strip()
    if len(PORT) <= 0:
        PORT = DEFAULT_PORT
    
    while True:
        try:
            print(aanderaa_4319a_read(PORT))
        except KeyboardInterrupt:
            print('user interrupted')
            break
