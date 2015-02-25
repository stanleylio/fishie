#!/usr/bin/python

# sample sensors, log to database and send to serial
# with node id, CRC32 checksum and formatted display
# note: terminal display != serial output

# TODO: allow missing sensor readings
# TODO: unsolicited broadcast vs. query-response
# TODO: detect and report capability (set of sensors/variables available)
# TODO: decouple transmission from sampling from storage
# TODO: individual sampling rates
# TODO: filtering for fast-changing variables, like water pressure and wind speed
# TODO: survive unplugging of any combination of sensors? depending on Linux' I2C driver

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

from __future__ import with_statement
import serial,time,sys,tzlocal
sys.path.append('drivers')
sys.path.append('storage')
import Adafruit_BBIO.UART as UART
from Adafruit_BMP085 import BMP085
from lib_si1145 import SI1145
from datetime import datetime
from ConfigParser import SafeConfigParser,NoSectionError
from ezo_ec import EZO_EC
from ezo_do import EZO_DO
from ezo_ph import EZO_pH
from ezo_orp import EZO_ORP
from ms5803_14ba import MS5803_14BA
from wind import Anemometer
from z import wrap,check                    # CRC checksum for comm link
from os.path import exists,join
from os import makedirs
from storage import storage

UART.setup('UART1')

#serial_name = 'COM4'
serial_name = '/dev/ttyO1'
#serial_name = '/dev/ttyUSB0'
baud = 9600                                 # I like 115200 better...

parser = SafeConfigParser()
parser.read('node_config.ini')
node_id = int(parser.get('node','id'))
wait = int(parser.get('node','wait'))

d = datetime.now()
count = 0
while d.year < 2015 and count < 60:     # heristics, hack-ish
    d = datetime.now()
    count = count + 1
    time.sleep(1)

bmp = BMP085(0x77,3)
si = SI1145()
ec = EZO_EC()
do = EZO_DO()
ph = EZO_pH()
orp = EZO_ORP()
ms = MS5803_14BA()
an = Anemometer()

store = storage()

try:
    with serial.Serial(serial_name,baud) as s:
        while True:
            # can get this in one call in Python 3.3. First time I see a reason to upgrade.
            #timestamp = (ts - datetime(1970,1,1).replace(tzinfo=pytz.timezone('UTC'))).total_seconds()
            # see also:
            #datetime.utcnow()

            ts_posix = time.time()
            #ts = datetime.fromtimestamp(ts_posix).replace(tzinfo=pytz.timezone('UTC'))
            #ts = datetime.fromtimestamp(ts_posix).replace(tzinfo=tzlocal.get_localzone())
            ts = datetime.fromtimestamp(ts_posix)
        
            bmptemp = bmp.readTemperature()
            bmppressure = bmp.readPressure()
            ectmp = ec.read()   # hum... I forgot each of these takes 1.3 second.
            dotmp = do.read()
            phtmp = ph.read()
            orptmp = orp.read()
            mstmp = ms.read()               # MS5803-14BA
            antmp = an.read()               # anemometer
            uvtmp = si.readUVIndex()        # Si1145
            irtmp = si.readIRLight()
            ambtmp = si.readAmbientLight()
            #print uvtmp,irtmp,ambtmp

            # display in terminal
            tmp = '{}, '.format(ts.strftime('%Y-%m-%d %H:%M:%S'))
            tmp = tmp + 'EC:{}uS, Sal.:{:.2f}, '.format(ectmp['ec'],ectmp['sal'])
            tmp = tmp + 'DO:{:.2f}uM, '.format(dotmp/32e-3)
            tmp = tmp + 'pH:{:.2f}, '.format(phtmp)
            tmp = tmp + 'ORP:{:.2f}mV, '.format(orptmp)
            tmp = tmp + 'Baro.P.:{:.2f}kPa, T.:{:.02f}Deg.C, '.format(bmppressure/1000.,bmptemp)
            tmp = tmp + 'Water P.:{}kPa, T.:{:.02f}Deg.C, '.format(mstmp['p'],mstmp['t'])
            tmp = tmp + '{:.1f}m/s, '.format(antmp)
            tmp = tmp + 'UV idx:{:.0f}, IR:{} lux, Amb.:{} lux'.format(uvtmp,irtmp,ambtmp)
            print tmp

            # send to serial port
            tmp = 'node_{:03d},{:.3f},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(\
                node_id,ts_posix,ectmp['ec'],ectmp['sal'],dotmp,phtmp,orptmp,
                bmppressure,bmptemp,            # BMP180
                mstmp['p'],mstmp['t'],          # MS5803-14BA
                antmp,                          # anemometer
                uvtmp,irtmp,ambtmp)             # Si1145

            tmp = wrap(tmp) + '\n'
            s.write(tmp)
            #print tmp.strip(),check(tmp)

            # log to local database
            # why doesn't the db complain about the POSIX float when the schema says datetime...
            '''tmp = (ts,
                   ectmp['ec'],ectmp['sal'],dotmp,phtmp,orptmp,
                   bmppressure,bmptemp,         # BMP180
                   mstmp['p'],mstmp['t'],       # MS5803-14BA
                   antmp,                       # anemometer
                   uvtmp,irtmp,ambtmp)          # Si1145'''
            d = {'Timestamp':ts,
                 'EZO_EC':ectmp['ec'],
                 'EZO_Sal':ectmp['sal'],
                 'EZO_DO':dotmp,
                 'EZO_pH':phtmp,
                 'EZO_ORP':orptmp,
                 'Pressure_BMP180':bmppressure,
                 'Temp_BMP180':bmptemp,
                 'Pressure_MS5803':mstmp['p'],
                 'Temp_MS5803':mstmp['t'],
                 'WindSpeed':antmp,
                 'UV_Si1145':uvtmp,
                 'IR_Si1145':irtmp,
                 'Amb_Si1145':ambtmp}
            #print tmp
            store.write(node_id,d)
            
            time.sleep(wait)
except KeyboardInterrupt:
    print 'user interrupted'

