#!/usr/bin/python
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2018
import serial, time, re, logging
from datetime import datetime


logger = logging.getLogger(__name__)


msgfield = ['date','time','Chlorophyll','Turbidity','Thermistor']
convf = [str,str,int,int,int]

def parse_eco_flntu(line):
    line = line.strip()
    r = '(?P<date>\d{2}/\d{2}/\d{2})\s+' +\
        '(?P<time>\d{2}:\d{2}:\d{2})\s+' +\
        '695\s+(?P<Chlorophyll>\d+)\s+' +\
        '700\s+(?P<Turbidity>\d+)\s+' +\
        '(?P<Thermistor>\d+)' +\
        '.*'
    r = re.match(r, line)
    if r is None:
        return r
    d = {}
    for k,c in enumerate(msgfield):
        d[c] = convf[k](r.group(c))
    #d['sensor_clock'] = datetime.strptime(d['date']+d['time'],'%m/%d/%y%H:%M:%S')
    #del d['date']
    #del d['time']
    return d

def flntus_read(port):
    with serial.Serial(port, 19200, timeout=1) as ser:
        ser.flushInput()
        ser.flushOutput()
        ser.write('$run\r\n'.encode())
        for i in range(15): # should be exactly 13 lines
            line = ser.readline().decode()
            logger.debug(line)
            tmp = parse_eco_flntu(line)
            if tmp is not None:
                return tmp
            else:
                logger.debug('waiting for sensor...')
    return None


if '__main__' == __name__:

    logging.basicConfig(level=logging.WARNING)
    
    while True:
        try:
            print(flntus_read('/dev/ttyO1'))
            time.sleep(5)
        except KeyboardInterrupt:
            break
