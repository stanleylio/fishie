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

from __future__ import with_statement
import Adafruit_BBIO.UART as UART
from Adafruit_BMP085 import BMP085
from lib_si1145 import SI1145
import serial,time
from datetime import datetime
from ConfigParser import SafeConfigParser,NoSectionError
from ezo_ec import EZO_EC
from ezo_do import EZO_DO
from ezo_ph import EZO_pH
from ezo_orp import EZO_ORP
from ms5803_14ba import MS5803_14BA
from wind import Anemometer
from z import wrap,check

UART.setup('UART1')

#serial_name = 'COM4'
serial_name = '/dev/ttyO1'
#serial_name = '/dev/ttyUSB0'
baud = 9600             # I like 115200 better...

parser = SafeConfigParser()
parser.read('node_config.ini')
ID = int(parser.get('node','id'))

bmp = BMP085(0x77,3)    # tradeoff of using someone else's library.
si = SI1145()

try:
    with serial.Serial(serial_name,baud) as s,\
         EZO_EC() as ec,\
         EZO_DO() as do,\
         EZO_pH() as ph,\
         EZO_ORP() as orp,\
         MS5803_14BA() as ms,\
         Anemometer() as an:
        
        while True:
            ts = time.time()
            bmptemp = bmp.readTemperature()
            bmppressure = bmp.readPressure()/100.
            ectmp = ec.read()   # hum... I forgot each of these takes 1.3 second.
            dotmp = do.read()
            phtmp = ph.read()
            orptmp = orp.read()
            mstmp = ms.read()
            antmp = an.read()
            uvtmp = si.readUVIndex()
            irtmp = si.readIRLight()
            ambtmp = si.readAmbientLight()

            print uvtmp,irtmp,ambtmp
            
            tmp = '{}, '.format(datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
            tmp = tmp + 'EC:{}uS, Sal.:{:.2f}, '.format(ectmp['ec'],ectmp['sal'])
            tmp = tmp + 'DO:{:.2f}uM, '.format(dotmp/32e-3)
            tmp = tmp + 'pH:{:.2f}, '.format(phtmp)
            tmp = tmp + 'ORP:{:.2f}mV, '.format(orptmp)
            tmp = tmp + 'Baro.P.:{:.2f}kPa, T.:{:.02f}Deg.C, '.format(bmppressure/10.,bmptemp)
            tmp = tmp + 'Water P.:{}kPa, T.:{:.02f}Deg.C, '.format(mstmp['p'],mstmp['t'])
            tmp = tmp + '{:.1f} m/s, '.format(antmp)
            tmp = tmp + 'UV idx:{:.0f}, IR:{} lux, Amb.:{} lux'.format(uvtmp,irtmp,ambtmp)
            print tmp
            
            tmp = 'node_{:03d},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(\
                ID,ts,ectmp['ec'],ectmp['sal'],
                dotmp,
                phtmp,
                orptmp,
                bmppressure,bmptemp,
                mstmp['p'],mstmp['t'],
                antmp,
                uvtmp,irtmp,ambtmp)

            tmp = wrap(tmp) + '\n'
            #print tmp
            s.write(tmp)
            #print tmp.strip(),check(tmp)
            
            #time.sleep(1)       # so this may not be necessary after all.
except KeyboardInterrupt:
    print 'user interrupted'
print 'closed'

