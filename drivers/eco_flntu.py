#!/usr/bin/python
#
# Interface wrapper for ECO FLNTU
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. March 2015
import serial,io,time,re
from datetime import datetime
from threading import Thread,Event


def PRINT(s):
    #pass
    print(s)

def parse_eco_flntu(line):
    msgfield = ['date','time','Chlorophyll','Turbidity','Thermistor']
    convf = [str,str,int,int,int]
    
    d = None
    try:
        line = line.strip()
        r = '(?P<date>\d{2}/\d{2}/\d{2})\s+' +\
            '(?P<time>\d{2}:\d{2}:\d{2})\s+' +\
            '695\s+(?P<Chlorophyll>\d+)\s+' +\
            '700\s+(?P<Turbidity>\d+)\s+' +\
            '(?P<Thermistor>\d+)' +\
            '.*'
        r = re.match(r,line)
        if r is not None:
            d = {}
            for k,c in enumerate(msgfield):
                d[c] = convf[k](r.group(c))
            d['FLNTU_Timestamp'] = datetime.strptime(d['date']+d['time'],'%m/%d/%y'+'%H:%M:%S')
    except Exception as e:
        PRINT('ECO_FLNTU(): cannot parse: {}'.format(line))
        PRINT(e)
    return d

class ECO_FLNTU(Thread):
    def __init__(self,port='/dev/ttyO2',baud=19200):
        super(ECO_FLNTU,self).__init__()
        self._d = None
        self._port = port
        self._baud = baud
        self._stop = Event()

        # so that if no other non-daemonic thread (such as main thread) is alive, this dies
        # without having someone else to call stop()
        self.daemon = True
        self.start()

    # TODO: throw warning when measurement is stale
    def read(self):
        return self._d
    
    def run(self):
        with serial.Serial(self._port,self._baud,timeout=2) as ser:
            ser.flushInput()
            ser.flushOutput()
            s = io.TextIOWrapper(io.BufferedRWPair(ser,ser,1),newline=None,encoding='ascii')

            while not self._stop.is_set():
                try:
                    line = s.readline().strip()
                    if len(line) > 0:
                        if line.startswith('vms'):
                            pass
                        else:
                            tmp = parse_eco_flntu(line)
                            if tmp is not None:
                                self._d = tmp
                except serial.SerialException:
                    PRINT('ECO_FLNTU: USB-to-serial converters are evil')
                except Exception as e:
                    PRINT('ECO_FLNTU::run(): unknown exception')
                    raise e
                
                time.sleep(1)
            PRINT('ECO_FLNTU: stopped')

    def stop(self):
        self._stop.set()

    def is_running(self):
        return not self._stop.is_set()


if '__main__' == __name__:
    print 'born'
    #line = '03/13/15        07:48:50        695     3941    700     4121    549'
    #print parse_eco_flntu(line)
    #exit()
    
    flntu = ECO_FLNTU()
    try:
        #for i in range(60):
        while True:
            tmp = flntu.read()
            print tmp
            time.sleep(1)
    except KeyboardInterrupt:
        print 'user interrupted'

    print 'die'
    # setting it as a daemon makes it terminates after main automatically so I don't even need
    # to call stop(). neat.
    #optode.stop()
    #print 'dead'


