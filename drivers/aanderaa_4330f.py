#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. August 2015
import serial,re,traceback,logging,time


logger = logging.getLogger(__name__)


def parse_4330f(line):
    d = None
    if len(line) and 'MEASUREMENT' in line and 'O2Concentration' and 'AirSaturation' in line:
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
            for k,c in enumerate(Aanderaa_4330f.msgfield):
                d[c] = Aanderaa_4330f.convf[k](r.group(c))
    return d


class Aanderaa_4330f(object):

    MAX_RETRY = 3
    
    msgfield = ['SN','O2Concentration','AirSaturation','Temperature','CalPhase',\
                'TCPhase','C1RPh','C2RPh','C1Amp','C2Amp','RawTemp']
    convf = [int,float,float,float,float,float,float,float,float,float,float]

    def __init__(self,port='/dev/ttyO4'):
        self._port = port
        with serial.Serial(self._port,9600,timeout=0.5) as s:
            s.write(b'\r\nreset\r\n')
            s.write(b'\r\ndo stop\r\n')
            s.flushOutput()

    def read(self):
        with serial.Serial(self._port,9600,timeout=0.2) as s:
            s.flushInput()
            s.flushOutput()
            # optode does not respond immediately after it wake up
            # so the first few commands will probably be lost
            # retry several times til a successful read is returned

            for i in range(self.MAX_RETRY):
                s.write(b'do sample\r\n')
                logger.debug('trial {}'.format(i))
                for j in range(15):
                    logger.debug('nope')
                    line = s.readline().decode().strip()
                    d = parse_4330f(line)
                    if d:
                        return d
            logger.error('Aanderaa_4330f::read(): no valid response from optode. (Check the output format setting of the optode?)')
        return None


if '__main__' == __name__:

    #w = 'MEASUREMENT     4330F   829     O2Concentration(uM)     264.241 AirSaturation(%)        99.637  Temperature(Deg.C)      23.458  CalPhase(Deg)   27.054  TCPhase(Deg)   30.149   C1RPh(Deg)      34.098  C2RPh(Deg)      3.949   C1Amp(mV)       594.7  C2Amp(mV)        697.2   RawTemp(mV)     181.7'
    #w = 'MEASUREMENT     4330F   829     O2Concentration(uM)     264.217 AirSaturation(%)        99.575  Temperature(Deg.C)      23.430  CalPhase(Deg)   27.066     TCPhase(Deg)    30.160  C1RPh(Deg)      34.107  C2RPh(Deg)      3.947   C1Amp(mV)       595.0   C2Amp(mV)       697.2   RawTemp(mV)     182.7'
    #w = 'MEASUREMENT	4330F	829	O2Concentration(uM)	263.870	AirSaturation(%)	99.293	Temperature(Deg.C)	23.349	CalPhase(Deg)	27.110	TCPhase(Deg)	30.200	C1RPh(Deg)	34.202	C2RPh(Deg)	4.002	C1Amp(mV)	595.3	C2Amp(mV)	697.2	RawTemp(mV)	185.3	'
    # new firmware, new format
    # w = 'MEASUREMENT	4330F	832	O2Concentration[uM]	299.573	AirSaturation[%]	111.641	Temperature[Deg.C]	22.893	CalPhase[Deg]	26.866	TCPhase[Deg]	28.905	C1RPh[Deg]	36.820	C2RPh[Deg]	7.915	C1Amp[mV]	3048.6	C2Amp[mV]	1312.1	RawTemp[mV]	88.3'
    #print Aanderaa_4330f.parse_4330f(w)
    #exit()

    logger.setLevel(logging.DEBUG)

    optode = Aanderaa_4330f(port='COM33')
        
    while True:
        try:
            print(optode.read())
        except KeyboardInterrupt:
            break
