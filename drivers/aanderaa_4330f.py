#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. August 2015
import serial,re,traceback


def PRINT(s):
    pass
    #print(s)


class Aanderaa_4330f(object):

    MAX_RETRY = 3
    
    msgfield = ['SN','O2Concentration','AirSaturation','Temperature','CalPhase',\
                'TCPhase','C1RPh','C2RPh','C1Amp','C2Amp','RawTemp']
    convf = [int,float,float,float,float,float,float,float,float,float,float]

    def __init__(self,port='/dev/ttyO4'):
        self._port = port
        with serial.Serial(self._port,9600,timeout=1) as s:
            s.write('\r\nreset\r\n')
            s.write('\r\ndo stop\r\n')
            s.flushInput()
            s.flushOutput()

    def read(self):
        try:
            with serial.Serial(self._port,9600,timeout=2) as s:
                s.flushInput()
                s.flushOutput()
                # optode does not respond immediately after it wake up
                # so the first few commands will probably be lost
                # retry several times til a successful read is returned

                count = 0
                s.write('\r\ndo stop\r\n')
                # should get a '#'
                while len(s.readline().strip()) <= 0 and count < self.MAX_RETRY:
                    s.write('\r\ndo stop\r\n')
                    count = count + 1
                    # relying on the timeout instead of using time.sleep()
                if count >= self.MAX_RETRY:
                    PRINT('Optode not responding to "do stop". Is it connected on {}?'.\
                          format(self._port))
                    return None
                    # still gonna try reading it anyway

                count = 0
                s.write('\r\ndo sample\r\n')
                line = s.readline()
                while '4330F' not in line and count < self.MAX_RETRY:
                    count = count + 1
                    line = s.readline()
                    return Aanderaa_4330f.parse_4330f(line)
                PRINT('Aanderaa_4330f::read(): no valid response from optode')
        except Exception:   # so that it doesn't capture KeyboardInterrupt
            traceback.print_exc()
        return None

    @staticmethod
    def parse_4330f(line):
        d = None
        try:
            line = line.strip()
            r = '.*MEASUREMENT\s+4330F\s+(?P<SN>\d+)\s+' +\
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
            r = re.match(r,line)
            if r is not None:
                d = {}
                for k,c in enumerate(Aanderaa_4330f.msgfield):
                    d[c] = Aanderaa_4330f.convf[k](r.group(c))
        except Exception as e:
            PRINT('parse_4330f(): cannot parse: {}'.format(line))
            PRINT(e)
        return d


if '__main__' == __name__:
    import time
    from os.path import exists

    #optode = Aanderaa_4330f(port='/dev/ttyO2')
    optode = Aanderaa_4330f(port='/dev/ttyO4')
    #optode = Aanderaa_4330f(port='COM11')
        
    try:
        while True:
            print optode.read()
            time.sleep(1)
    except KeyboardInterrupt:
        print 'user interrupted'

