#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. August 2015
import serial, re, logging, time


logger = logging.getLogger(__name__)


msgfield = ['SN', 'O2Concentration', 'AirSaturation', 'Temperature', 'CalPhase',\
            'TCPhase', 'C1RPh', 'C2RPh', 'C1Amp', 'C2Amp', 'RawTemp']
convf = [int, float, float, float, float, float, float, float, float, float, float]


def parse_4330f(line):
    
    d = None
    line = line.strip()
    '''r = '.*MEASUREMENT\s+4330F\s+(?P<SN>\d+)\s+' +\
          'O2Concentration\(uM\)\s+(?P<O2Concentration>[+-]*\d+\.*\d*)\s+' +\
          'AirSaturation\(\%\)\s+(?P<AirSaturation>[+-]*\d+\.*\d*)\s+' +\
          'Temperature\(Deg\.C\)\s+(?P<Temperature>[+-]*\d+\.*\d*)\s+' +\
          'CalPhase\(Deg\)\s+(?P<CalPhase>[+-]*\d+\.*\d*)\s+' +\
          'TCPhase\(Deg\)\s+(?P<TCPhase>[+-]*\d+\.*\d*)\s+' +\
          'C1RPh\(Deg\)\s+(?P<C1RPh>[+-]*\d+\.*\d*)\s+' +\
          'C2RPh\(Deg\)\s+(?P<C2RPh>[+-]*\d+\.*\d*)\s+' +\
          'C1Amp\(mV\)\s+(?P<C1Amp>[+-]*\d+\.*\d*)\s+' +\
          'C2Amp\(mV\)\s+(?P<C2Amp>[+-]*\d+\.*\d*)\s+' +\
          'RawTemp\(mV\)\s+(?P<RawTemp>[+-]*\d+\.*\d*).*'
          '''
    # new firmware, new format
    r = '.*MEASUREMENT\s+4330F\s+(?P<SN>\d+)\s+' +\
          'O2Concentration\[uM\]\s+(?P<O2Concentration>[+-]*\d+\.*\d*)\s+' +\
          'AirSaturation\[%\]\s+(?P<AirSaturation>[+-]*\d+\.*\d*)\s+' +\
          'Temperature\[Deg\.C\]\s+(?P<Temperature>[+-]*\d+\.*\d*)\s+' +\
          'CalPhase\[Deg\]\s+(?P<CalPhase>[+-]*\d+\.*\d*)\s+' +\
          'TCPhase\[Deg\]\s+(?P<TCPhase>[+-]*\d+\.*\d*)\s+' +\
          'C1RPh\[Deg\]\s+(?P<C1RPh>[+-]*\d+\.*\d*)\s+' +\
          'C2RPh\[Deg\]\s+(?P<C2RPh>[+-]*\d+\.*\d*)\s+' +\
          'C1Amp\[mV\]\s+(?P<C1Amp>[+-]*\d+\.*\d*)\s+' +\
          'C2Amp\[mV\]\s+(?P<C2Amp>[+-]*\d+\.*\d*)\s+' +\
          'RawTemp\[mV\]\s+(?P<RawTemp>[+-]*\d+\.*\d*).*'
    r = re.match(r,line)
    if r is not None:
        d = {}
        for k,c in enumerate(msgfield):
            d[c] = convf[k](r.group(c))
    return d


def aanderaa_4330f_read(port, max_retry=5):
    logger.debug('aanderaa_4330f_read()')
    
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
                        r = parse_4330f(line)
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

    #w = 'MEASUREMENT     4330F   829     O2Concentration(uM)     264.241 AirSaturation(%)        99.637  Temperature(Deg.C)      23.458  CalPhase(Deg)   27.054  TCPhase(Deg)   30.149   C1RPh(Deg)      34.098  C2RPh(Deg)      3.949   C1Amp(mV)       594.7  C2Amp(mV)        697.2   RawTemp(mV)     181.7'
    #w = 'MEASUREMENT     4330F   829     O2Concentration(uM)     264.217 AirSaturation(%)        99.575  Temperature(Deg.C)      23.430  CalPhase(Deg)   27.066     TCPhase(Deg)    30.160  C1RPh(Deg)      34.107  C2RPh(Deg)      3.947   C1Amp(mV)       595.0   C2Amp(mV)       697.2   RawTemp(mV)     182.7'
    #w = 'MEASUREMENT	4330F	829	O2Concentration(uM)	263.870	AirSaturation(%)	99.293	Temperature(Deg.C)	23.349	CalPhase(Deg)	27.110	TCPhase(Deg)	30.200	C1RPh(Deg)	34.202	C2RPh(Deg)	4.002	C1Amp(mV)	595.3	C2Amp(mV)	697.2	RawTemp(mV)	185.3	'
    # new firmware, new format
    # w = 'MEASUREMENT	4330F	832	O2Concentration[uM]	299.573	AirSaturation[%]	111.641	Temperature[Deg.C]	22.893	CalPhase[Deg]	26.866	TCPhase[Deg]	28.905	C1RPh[Deg]	36.820	C2RPh[Deg]	7.915	C1Amp[mV]	3048.6	C2Amp[mV]	1312.1	RawTemp[mV]	88.3'
    #print(parse_4330f(w))

    logger.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)

    DEFAULT_PORT = '/dev/ttyS1'
    PORT = input('PORT=? (default={})'.format(DEFAULT_PORT)).strip()
    if len(PORT) <= 0:
        PORT = DEFAULT_PORT

    while True:
        try:
            print(aanderaa_4330f_read(PORT))
        except KeyboardInterrupt:
            print('user interrupted')
            break
