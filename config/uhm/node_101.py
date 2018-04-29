# -*- coding: utf-8 -*-
name = '"Guac-is-Extra"'
location = '(TBD)'
note = 'Beaglebone-based node measuring oxygen, temperature, conductivity, and pressure'

# node stuff
XBEE_PORT = '/dev/ttyS2'
XBEE_BAUD = 115200

XBEELOGDIR = '/var/uhcm/log'

INTERVAL = 5*60
NGROUP = 5

#LOGDIR = '/var/uhcm/log'
dbfile = '/var/uhcm/storage/sensor_data.db'
subscribeto = ['127.0.0.1:9002']


conf = [
    {
        'dbtag':'ts',
        'description':'Time of sampling (device clock)',
        'plot':True,
    },
    {
        'dbtag':'P_280',
        'unit':'kPa',
        'description':'Barometric pressure (BMP280)',
        'lb':90e3,
        'ub':110e3,
    },
    {
        'dbtag':'T_280',
        'unit':'Deg.C',
        'description':'Enclosure temperature (BMP280)',
        'lb':-10,
        'ub':70,
    },
    {
        'dbtag':'P_5803',
        'unit':'kPa',
        'description':'Water pressure (MS5803-14BA)',
        'lb':90,
        'ub':150,
    },
    {
        'dbtag':'T_5803',
        'unit':'Deg.C',
        'description':'Water temperature (MS5803-14BA)',
        'lb':-10,
        'ub':50,
    },
    {
        'dbtag':'DO',
        'unit':'uM',
        'description':'Oxygen concentration',
        'lb':0,
        'ub':400,
    },
    {
        'dbtag':'T_optode',
        'unit':'Deg.C',
        'description':'Water temperature (optode)',
        'lb':-10,
        'ub':50,
    },
    {
        'dbtag':'AirSat',
        'unit':'%',
        'description':'Air saturation',
        'lb':0,
        'ub':130,
    },
    {
        'dbtag':'EC',
        'unit':'mS/cm',
        'description':'Electrical Conductivity',
        'lb':0,
    },
    {
        'dbtag':'T_ec',
        'unit':'Deg.C',
        'description':'Water temperature (conductivity probe)',
        'lb':-10,
        'ub':50,
    },
]


if '__main__' == __name__:
    for c in conf:
        print('- - -')
        for k, v in c.items():
            print(k, ':', v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf, basename(__file__).split('.')[0].replace('_', '-'))
