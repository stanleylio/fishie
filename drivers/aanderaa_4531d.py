# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2018
import re, logging


logger = logging.getLogger(__name__)


def parse_4531d(line):
    msgfield = ['SN', 'O2Concentration', 'AirSaturation', 'Temperature']
    convf = [int, float, float, float]
    convf = dict(zip(msgfield, convf))
    
    d = None
    line = line.strip()
    r = '.*MEASUREMENT\s+4531\s+(?P<SN>\d+)\s+' +\
          'O2Concentration\[uM\]\s+(?P<O2Concentration>[+-]*\d+\.*\d*)\s+' +\
          'AirSaturation\[%\]\s+(?P<AirSaturation>[+-]*\d+\.*\d*)\s+' +\
          'Temperature\[Deg\.C\]\s+(?P<Temperature>[+-]*\d+\.*\d*).*'
    r = re.match(r, line)
    if r:
        return {k:convf[k](v) for k,v in r.groupdict().items()}
    else:
        logger.debug('Format mismatch: {}'.format(line))
        logger.debug([ord(c) for c in line])
    return d


def aanderaa_4531d_read(port, max_retry=5):
    from . import aanderaa
    return aanderaa.aanderaa_read_universal(port, max_retry=max_retry, parsers=[parse_4531d])
    

if '__main__' == __name__:

    '''MEASUREMENT	4531	395	O2Concentration[uM]	259.160	AirSaturation[%]	97.999	Temperature[Deg.C]	23.662
MEASUREMENT	4531	395	O2Concentration[uM]	259.050	AirSaturation[%]	97.957	Temperature[Deg.C]	23.662
MEASUREMENT	4531	395	O2Concentration[uM]	258.975	AirSaturation[%]	97.928	Temperature[Deg.C]	23.661
MEASUREMENT	4531	395	O2Concentration[uM]	259.072	AirSaturation[%]	97.956	Temperature[Deg.C]	23.657
MEASUREMENT	4531	395	O2Concentration[uM]	259.197	AirSaturation[%]	97.994	Temperature[Deg.C]	23.652
MEASUREMENT	4531	395	O2Concentration[uM]	259.092	AirSaturation[%]	97.947	Temperature[Deg.C]	23.648
MEASUREMENT	4531	395	O2Concentration[uM]	258.967	AirSaturation[%]	97.899	Temperature[Deg.C]	23.647
'''

    #print(parse_4531d(' MEASUREMENT  4531    395     O2Concentration[uM]     261.334 AirSaturation[%]     98.142  Temperature[Deg.C]      23.297'))
    #exit()
    
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)

    DEFAULT_PORT = '/dev/ttyS1'
    PORT = input('PORT=? (default={})'.format(DEFAULT_PORT)).strip()
    if len(PORT) <= 0:
        PORT = DEFAULT_PORT

    while True:
        try:
            print(aanderaa_4531d_read(PORT))
        except KeyboardInterrupt:
            print('user interrupted')
            break
