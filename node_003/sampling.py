#!/usr/bin/python

# sample sensors, log to database and send to serial
# with node id, CRC32 checksum and formatted display
# note: terminal display != serial output

# a thought, just a thought... what if I include the name of the fields in the serial data...
# more data to send and more prone to loss, but much easier to parse.

# TODO: allow missing sensor/readings!!!
# TODO: unsolicited broadcast vs. query-response
# TODO: detect and report capability (set of sensors/variables available)
# TODO: decouple transmission from sampling from storage
# TODO: individual sampling rates
# TODO: filtering for fast-changing variables, like water pressure and wind speed
# TODO: survive unplugging of any combination of sensors? depending on Linux' I2C driver

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. March 2015

import serial,time,sys
sys.path.append('drivers')
sys.path.append('storage')
import Adafruit_BBIO.UART as UART
from datetime import datetime
from aanderaa_4330f import Aanderaa_4330f
from z import check,get_checksum
from os.path import exists,join
from os import makedirs
from storage import storage
from config_support import read_config
from parse_support import pretty_print


# wait at most 1 minute for the system clock to initialize (ntpdate, hwclock etc.)
d = datetime.now()
count = 0
while d.year < 2015 and count < 60:     # heristics, hack-ish
    d = datetime.now()
    count = count + 1
    time.sleep(1)

# find out the ID and capability of this node
tmp = read_config()
broadcast_port = tmp['node']['broadcast_port']
broadcast_baud = tmp['node']['broadcast_baud']
node_id = int(tmp['node']['id'])
wait = int(tmp['node']['wait'])

node_tag = 'node_{:03d}'.format(node_id)
msgfield = [s.strip() for s in tmp[node_tag]['msgfield'].split(',')]
try:
    optode_port = tmp[node_tag]['optode_port']
    if not exists(optode_port):
        optode_port = None
except KeyError:
    optode_port = None

# hardware-related
UART.setup('UART1')

print 'waiting for optode at {}...'.format(optode_port)
optode = Aanderaa_4330f(port=optode_port)   # this one sure is slow...

store = storage()

try:
    with serial.Serial(broadcast_port,broadcast_baud) as s:
        while True:
            # can get this in one call in Python 3.3. First time I see a reason to upgrade.
            #timestamp = (ts - datetime(1970,1,1).replace(tzinfo=pytz.timezone('UTC'))).total_seconds()
            # see also:
            #datetime.utcnow()

            ts_posix = time.time()
            #ts = datetime.fromtimestamp(ts_posix).replace(tzinfo=pytz.timezone('UTC'))
            #ts = datetime.fromtimestamp(ts_posix).replace(tzinfo=tzlocal.get_localzone())
            ts = datetime.fromtimestamp(ts_posix)

            # "whenever you find yourself copy and paste -ing code, stop and think"
            # yeah I think it's due for a major rewrite again. with an abstraction called
            # "data source" or "variable" which carries its own name, unit, conversion
            # function and format etc. and the logger can just get a list of these "data
            # sources" and access them uniformly.
            # dbtags on the left, msgfield on the
            # rule: if it is deterministic, it can be automated.
            # TODO
            # hum... how about this: the logger "do sample" by:
            #   for each variable v:
            #       invoke the registered function: datasource[v]()
            # say EZO_EC: register with the logger its read_ec() using the dbtag 'EZO_EC',
            # something like
            #   logger.register('EZO_EC',ezo_ec.read_ec)
            # but EZO_EC gives you all four ec, sal, tds and sg in one go. how to split the
            #   read()
            # into four
            #   read_ec(), read_sal(), read_tds(), and read_sg()?
            # what about conversion functions? like mg/L to uM, Pa to kPa?
            optodetmp = optode.read()
            O2Concentration_4330f = optodetmp['O2Concentration']
            AirSaturation_4330f = optodetmp['AirSaturation']
            Temperature_4330f = optodetmp['Temperature']
            CalPhase_4330f = optodetmp['CalPhase']
            TCPhase_4330f = optodetmp['TCPhase']
            C1RPh_4330f = optodetmp['C1RPh']
            C2RPh_4330f = optodetmp['C2RPh']
            C1Amp_4330f = optodetmp['C1Amp']
            C2Amp_4330f = optodetmp['C2Amp']
            RawTemp_4330f = optodetmp['RawTemp']

            d = {'Timestamp':ts,
                 'O2Concentration_4330f':O2Concentration_4330f,
                 'AirSaturation_4330f':AirSaturation_4330f,
                 'Temperature_4330f':Temperature_4330f,
                 'CalPhase_4330f':CalPhase_4330f,
                 'TCPhase_4330f':TCPhase_4330f,
                 'C1RPh_4330f':C1RPh_4330f,
                 'C2RPh_4330f':C2RPh_4330f,
                 'C1Amp_4330f':C1Amp_4330f,
                 'C2Amp_4330f':C2Amp_4330f,
                 'RawTemp_4330f':RawTemp_4330f}

            # display in terminal
            pretty_print(d)
            '''print '= '*40
            print '{}'.format(ts.strftime('%Y-%m-%d %H:%M:%S'))
            print 'Elec. Conductivity: {} uS, Salinity : {:.2f}'.format(ec_ec,ec_sal)
            print 'DO: {:.2f} uM'.format(do_do/32e-3)
            print 'pH: {:.2f}'.format(ph_ph)
            print 'ORP: {:.2f}mV'.format(orp_orp)
            print 'BMP180 barometric pressure: {:.2f} kPa, Temperature: {:.02f} Deg.C'.\
                  format(bmp_p/1000.,bmp_t)
            print 'MS5803-14BA (water) pressure: {} kPa, Temperature: {:.02f} Deg.C'.\
                  format(ms_p,ms_t)
            print 'Wind speed: {:.1f} m/s'.format(an_windspeed)
            print 'IR: {} lux, Amb.: {} lux'.format(si_uv,si_ir,si_amb)
            print 'Optode O2Concentration: {} uM, AirSaturation: {}%, Temperature: {} Deg.C'.\
                  format(O2Concentration_4330f,AirSaturation_4330f,Temperature_4330f)'''

            # send to serial port
            ts_str = '{:.6f}'.format(ts_posix)
            readings = [node_tag,ts_str,
                O2Concentration_4330f,AirSaturation_4330f,Temperature_4330f,
                CalPhase_4330f,TCPhase_4330f,
                C1RPh_4330f,C2RPh_4330f,C1Amp_4330f,C2Amp_4330f,RawTemp_4330f]
            readings = [str(r) for r in readings]
            tmp = ','.join(readings)

            cs = get_checksum(tmp)
            tmp = '{},{}\n'.format(tmp,cs)
            s.write(tmp)

            # log to local database
            store.write(node_id,d)
            
            time.sleep(wait)
except KeyboardInterrupt:
    print 'user interrupted'

