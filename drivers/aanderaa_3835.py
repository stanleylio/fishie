#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. September 2015
import serial,re,traceback,logging


def parse_3835(line):
    d = None
    try:
        line = line.strip()
        r = '.*MEASUREMENT\s+3835\s+(?P<SN>\d+)\s+' +\
              'Oxygen\:\s+(?P<O2Concentration>[+-]*\d+\.*\d*)\s+' +\
              'Saturation\:\s+(?P<AirSaturation>[+-]*\d+\.*\d*)\s+' +\
              'Temperature\:\s+(?P<Temperature>[+-]*\d+\.*\d*).*'
        r = re.match(r,line)
        if r is not None:
            d = {}
            for k,c in enumerate(Aanderaa_3835.msgfield):
                d[c] = Aanderaa_3835.convf[k](r.group(c))
    except:
        logging.debug('parse_3835(): cannot parse: {}'.format(line))
        logging.debug(traceback.format_exc())
    return d


class Aanderaa_3835(object):

    MAX_RETRY = 3

    msgfield = ['O2Concentration','AirSaturation','Temperature']
    convf = [float,float,float]

    def __init__(self,port='/dev/ttyO4'):
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
                # optode does not respond immediately after it wake up
                # so the first few commands will probably be lost
                # retry several times til a successful read is returned

                count = 0
                s.write('\r\ndo stop\r\n')
                # should at least get a '#'
                while len(s.readline().strip()) <= 0:
                    s.write('\r\ndo stop\r\n')
                    count = count + 1
                    # relying on the timeout instead of using time.sleep()
                    if count > self.MAX_RETRY:
                        logging.debug('Optode not responding to "do stop". Is it connected on {}?'.format(self._port))
                        return None

                s.write('\r\ndo sample\r\n')
                for i in range(10):
                    line = s.readline()
                    #print line
                    tmp = parse_3835(line)
                    if tmp is not None:
                        return tmp

                logging.error('Aanderaa_3835::read(): no valid response from optode. (Check the output format setting of the optode?)')
        except:
            logging.debug(traceback.format_exc())
        return None


if '__main__' == __name__:
    
    #c1 = 'MEASUREMENT	  3835	   506	Oxygen: 	   264.81	Saturation: 	    90.54	Temperature: 	    18.47'
    #c2 = 'MEASUREMENT	  3835	   505	Oxygen: 	   287.81	Saturation: 	    95.10	Temperature: 	    16.82'
    #c3 = 'only nixon can go to china'
    #print parse_3835(c1)
    #print parse_3835(c2)
    #print parse_3835(c3)

    import time
    optode = Aanderaa_3835(port='/dev/ttyO2')
    while True:
        try:
            print optode.read()
            time.sleep(1)
        except KeyboardInterrupt:
            print 'user interrupted'
            break
