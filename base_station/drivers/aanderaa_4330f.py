#!/usr/bin/python
#
# Interface wrapper for the Aanderaa 4330F optode
#
# NOTE: It uses an internal thread to poll the optode periodically, so it is reading the
# optode even when no read() is called (don't be alarmed if you see more than one "do sample")
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. March 2015
import serial,io,time,re
from datetime import datetime
from threading import Thread,Event

def PRINT(s):
    pass
    #print(s)

def parse_4330f(line):
    msgfield = ['SN','O2Concentration','AirSaturation','Temperature','CalPhase','TCPhase','C1RPh','C2RPh','C1Amp','C2Amp','RawTemp']
    convf = [int,float,float,float,float,float,float,float,float,float,float]

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
            for k,c in enumerate(msgfield):
                d[c] = convf[k](r.group(c))
    except Exception as e:
        PRINT('parse_4330f(): cannot parse: {}'.format(line))
        PRINT(e)
    return d


class Aanderaa_4330f(Thread):
    def __init__(self,port='/dev/ttyUSB0',baud=9600):
        super(Aanderaa_4330f,self).__init__()
        self._d = None
        self._port = port
        self._baud = baud
        self._stop = Event()
        # so that if no other non-daemonic thread (such as main thread) is alive, this dies
        # without having someone else to call stop()
        self.daemon = True
        self.start()
        PRINT('Aanderaa_4330f: initializing...')
        for i in range(30):
            if self.read() is not None:
                break
            time.sleep(0.5)
        if self.read() is None:
            raise Exception('Aanderaa_4330f: unable to read from optode')

    def read(self):
        return self._d
    
    def run(self):
        with serial.Serial(self._port,self._baud,timeout=2) as ser:
            ser.flushInput()
            ser.flushOutput()
            s = io.TextIOWrapper(io.BufferedRWPair(ser,ser,1),newline=None,encoding='ascii')

            PRINT('Aanderaa_4330f: reset...')
            s.write(u'reset\r')
            # ignore the optode's response to 'reset'
            # need only one readline, so this is conservative...
            # the timeout=N is essential
            for i in range(3):
                line = s.readline()

            while not self._stop.is_set():
                try:
                    PRINT('Aanderaa_4330f: do sample...')
                    s.write(u'do sample\r')
                    for i in range(3):
                        line = s.readline().strip()
                        #print line
                        # evil heristic for performance. the optode spits out lots of
                        # garbage (line controls, '#', '*' etc.)
                        if len(line) > 10:
                            tmp = parse_4330f(line)
                            if tmp is not None:
                                tmp['Timestamp'] = datetime.utcnow()
                                #PRINT(tmp)
                                self._d = tmp
                                break
                except serial.SerialException:
                    PRINT('Aanderaa_4330f: USB-to-serial converters are evil')
                except Exception as e:
                    PRINT('Aanderaa_4330f::run(): unknown exception')
                    raise e
                
                time.sleep(1)   # hum... power vs. freshness tradeoff. TODO.
            PRINT('Aanderaa_4330f: stopped')

    def stop(self):
        self._stop.set()

    def is_running(self):
        return not self._stop.is_set()


if '__main__' == __name__:
    print 'born'
    optode = Aanderaa_4330f()
    try:
        #for i in range(60):
        while True:
            tmp = optode.read()
            if tmp is not None:
                print tmp
            time.sleep(1)
    except KeyboardInterrupt:
        print 'user interrupted'

    print 'die'
    # setting it as a daemon makes it terminates after main automatically so I don't even need
    # to call stop(). neat.
    #optode.stop()
    #print 'dead'


