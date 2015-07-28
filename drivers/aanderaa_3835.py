#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. September 2015
import serial,re,traceback

def PRINT(s):
    #pass
    print(s)

class Aanderaa_3835(object):
    msgfield = ['Oxygen','Saturation','Temperature']
    convf = [float,float,float]

    '''def __init__(self,port='/dev/ttyO2'):
        self._port = port
        with serial.Serial(self._port,9600,timeout=1) as s:
            s.write('\r\nreset\r\n')
            s.write('\r\ndo stop\r\n')
            s.flushInput()
            s.flushOutput()

    def read(self):
        try:
            with serial.Serial(self._port,9600,timeout=1) as s:
                s.flushInput()
                s.flushOutput()
                s.write('do stop\r\n')
                for j in range(5):
                    PRINT('{} try'.format(j+1))
                    s.write('do sample\r\n')
                    for i in range(5):
                        line = s.readline()
                        #print line
                        tmp = Aanderaa_3835.parse_3835(line)
                        if tmp is not None:
                            return tmp
                PRINT('Aanderaa_3835::read(): no valid response from optode')
        except Exception:
            traceback.print_exc()
        return None'''

    @staticmethod
    def parse_3835(line):
        d = None
        try:
            line = line.strip()
            r = '.*MEASUREMENT\s+3835\s+(?P<SN>\d+)\s+' +\
                  'Oxygen\:\s+(?P<Oxygen>[+-]*\d+\.*\d*)\s+' +\
                  'Saturation\:\s+(?P<Saturation>[+-]*\d+\.*\d*)\s+' +\
                  'Temperature\:\s+(?P<Temperature>[+-]*\d+\.*\d*).*'
            r = re.match(r,line)
            if r is not None:
                d = {}
                for k,c in enumerate(Aanderaa_3835.msgfield):
                    d[c] = Aanderaa_3835.convf[k](r.group(c))
        except Exception as e:
            PRINT('parse_3835(): cannot parse: {}'.format(line))
            PRINT(e)
        return d


if '__main__' == __name__:
    c1 = 'MEASUREMENT	  3835	   506	Oxygen: 	   264.81	Saturation: 	    90.54	Temperature: 	    18.47'
    c2 = 'MEASUREMENT	  3835	   505	Oxygen: 	   287.81	Saturation: 	    95.10	Temperature: 	    16.82'
    c3 = 'only nixon can go to china'

    optode = Aanderaa_3835()
    print optode.parse_3835(c1)
    print optode.parse_3835(c2)
    print optode.parse_3835(c3)

    optode = Aanderaa_3835(port='/dev/ttyO2')
    try:
        while True:
            print optode.read()
    except KeyboardInterrupt:
        print 'user interrupted'

