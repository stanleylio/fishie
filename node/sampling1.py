#!/usr/bin/python

# sample sensors and send to serial
# with node id
# with checksum
# better formatted display
# terminal display != serial output

# TODO: allow missing sensor readings
# TODO: survive hotplug/unplug of any combination of sensors
# TODO: log
# TODO: local RRD-like database
# TODO: decouple transmission from sampling
# TODO: individual sampling rates
# TODO: filtering for fast-changing variables, like water pressure and wind speed

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

import Adafruit_BBIO.UART as UART
from ezo_ec import EZO_EC
from ezo_do import EZO_DO
from ms5803_14ba import MS5803_14BA
from Adafruit_BMP085 import BMP085
import serial,time
from datetime import datetime
from ConfigParser import SafeConfigParser,NoSectionError
from z import wrap,check

UART.setup('UART1')

#serial_name = 'COM4'
serial_name = '/dev/ttyO1'
#serial_name = '/dev/ttyUSB0'
baud = 9600             # I like 115200 better...

bmp = BMP085(0x77, 3)   # ULTRAHIRES Mode

parser = SafeConfigParser()
parser.read('node_config.ini')
ID = int(parser.get('node','id'))

try:
    with serial.Serial(serial_name,baud) as s,\
         EZO_EC() as ec,\
         EZO_DO() as do,\
         MS5803_14BA() as ms:
        while True:
            ts = time.time()
            bmptemp = bmp.readTemperature()
            bmppressure = bmp.readPressure()/100.
            ectmp = ec.read()   # hum... I forgot each of these takes 1.3 second.
            dotmp = do.read()
            mstmp = ms.read()
            
            #print '{}, EC:{}uS, EC:{}, DO:{}mg/L, Baro.P.: {}hPa, Air.Temp.: {}Deg.C'.format(\
            #    datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'),\
            #    ectmp['ec'],ectmp['sal'],dotmp,bmppressure,bmptemp)
            print '{}\tEC:{}uS\tSal.:{:.2f}\tDO:{:.2f}uM\tBaro.P.:{:.2f}kPa\tAir T.:{}Deg.C\tWater.P.:{}kPa\tWater T.:{}Deg.C'.\
                  format(datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'),\
                ectmp['ec'],ectmp['sal'],dotmp/32e-3,bmppressure/10.,bmptemp,mstmp['p'],mstmp['t'])

            tmp = 'node_{:03d},{},{},{},{},{},{},{},{}'.format(\
                ID,ts,ectmp['ec'],ectmp['sal'],dotmp,bmppressure,bmptemp,mstmp['p'],mstmp['t'])

            tmp = wrap(tmp) + '\n'
            #print tmp
            s.write(tmp)
            #print tmp.strip(),check(tmp)
            
            #time.sleep(1)       # so this may not be necessary after all.
except KeyboardInterrupt:
    print 'user interrupted'
print 'closed'

