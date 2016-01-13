#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. August 2015
import serial,time,re
from datetime import datetime

def PRINT(s):
    pass
    #print(s)


class ECO_FLNTU(object):
    def __init__(self,port='/dev/ttyO2'):
        self._port = port
        self.msgfield = ['date','time','Chlorophyll','Turbidity','Thermistor']
        self.convf = [str,str,int,int,int]

    def read(self):
        try:
            with serial.Serial(self._port,19200,timeout=1) as s:
                s.flushInput()
                s.flushOutput()
                s.write('$run\r\n')
                for i in range(15): # should be exactly 13 lines
                    line = s.readline()
                    tmp = self.parse_eco_flntu(line)
                    if tmp is not None:
                        return tmp
                    else:
                        PRINT('ECO_FLNTU(): waiting for sensor...')
        except Exception as e:
            PRINT(e)
        return None

    def parse_eco_flntu(self,line):
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
                for k,c in enumerate(self.msgfield):
                    d[c] = self.convf[k](r.group(c))
                #d['FLNTU_Timestamp'] = datetime.strptime(d['date']+d['time'],'%m/%d/%y'+'%H:%M:%S')
                #del d['date']
                #del d['time']
            return d
        except:
            return None


if '__main__' == __name__:
    #flntu = ECO_FLNTU(port='COM3')
    flntu = ECO_FLNTU(port='/dev/ttyO2')
    try:
        while True:
            tmp = flntu.read()
            print tmp
            time.sleep(5)
    except KeyboardInterrupt:
        print 'user interrupted'





    
