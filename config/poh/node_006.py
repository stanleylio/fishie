# -*- coding: utf-8 -*-
name = 'Met Station #2'
location = 'First Mākāhā'
note = 'Beaglebone with an RM Young Anemometer, Bosch Temperature/Humidity/Pressure and light intensity'

# node stuff
XBEE_PORT = '/dev/ttyO1'
XBEE_BAUD = 115200

XBEELOGDIR = '/var/uhcm/log'

INTERVAL = 1
NGROUP = 1

#dbfile = '/var/uhcm/storage/sensor_data.db'
subscribeto = ['127.0.0.1:9002']


conf = [
    {
        'dbtag':'Timestamp',
        'dbtype':'DOUBLE NOT NULL',
        'description':'Time of sampling',
        'plot':False,
    },
    {
        'dbtag':'wind_mps',
        'description':'Wind speed',
        'unit':'m/s',
        'lb':0,
    },
    {
        'dbtag':'wind_dir_deg',
        'description':'Wind direction',
        'unit':'Deg',
        'lb':0,
        'ub':360,
    },
    {
        'dbtag':'P_180',
        'unit':'Pa',
        'description':'Barometric pressure (BMP180)',
        'lb':80e3,
        'ub':110e3,
    },
    {
        'dbtag':'T_180',
        'unit':'Deg.C',
        'description':'Enclosure temperature (BMP180)',
        'lb':0,
        'ub':80,
    },
    {
        'dbtag':'P_280',
        'unit':'kPa',
        'description':'Barometric pressure (BME280)',
        'lb':80,
        'ub':110,
    },
    {
        'dbtag':'T_280',
        'unit':'Deg.C',
        'description':'Air temperature (BME280)',
        'lb':0,
        'ub':50,
    },
    {
        'dbtag':'RH_280',
        'unit':'%',
        'description':'% Relative humidity (BME280)',
        'lb':0,
        'ub':100,
    },
    {
        'dbtag':'UV_Si1145',
        'unit':'(100x index)',
        'description':'UV Index x 100',
    },
    {
        'dbtag':'IR_Si1145',
        'unit':'lux',
        'description':'IR',
    },
    {
        'dbtag':'Amb_Si1145',
        'unit':'lux',
        'description':'Ambient light intensity',
    },
    {
        'dbtag':'CH0_TSL2591',
        'description':'CH0 of TSL2591',
    },
    {
        'dbtag':'CH1_TSL2591',
        'description':'CH1 of TSL2591',
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table

    conf.insert(0,{'dbtag':'ReceptionTime','dbtype':'DOUBLE NOT NULL'})
    create_table(conf,basename(__file__).split('.')[0].replace('_','-'))
