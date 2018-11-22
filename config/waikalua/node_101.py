# -*- coding: utf-8 -*-
name = 'Limu Wai CTD-O2'
location = 'Waikalua Loko I`a (21.411111, -157.784167)'
note = 'Beaglebone-based node measuring oxygen, temperature, conductivity, and pressure'

# node stuff
XBEE_PORT = '/dev/ttyS2'
XBEE_BAUD = 115200

#XBEELOGDIR = '/var/uhcm/log'

INTERVAL = 5*60
NGROUP = 5

subscribeto = ['127.0.0.1:9002']


conf = [
    {
        'dbtag':'ts',
        'description':'Time of sampling (device clock)',
        'plot':True,
        'interval':180,
    },
    {
        'dbtag':'Pa',
        'unit':'kPa',
        'description':'Barometric pressure (BME280)',
        'lb':90,
        'ub':110,
        'interval':180,
    },
    {
        'dbtag':'Ta',
        'unit':'Deg.C',
        'description':'Enclosure temperature (BME280)',
        'lb':-10,
        'ub':70,
        'interval':180,
    },
    {
        'dbtag':'RH',
        'unit':'%',
        'description':'Enclosure humidity (BME280)',
        'lb':20,
        'ub':90,
        'interval':180,
    },
    {
        'dbtag':'Pw',
        'unit':'kPa',
        'description':'Water pressure (MS5803-14BA)',
        'lb':90,
        'ub':150,
        'interval':180,
    },
    {
        'dbtag':'Tw',
        'unit':'Deg.C',
        'description':'Water temperature (MS5803-14BA)',
        'lb':-10,
        'ub':50,
        'interval':180,
    },
    {
        'dbtag':'DO',
        'unit':'uM',
        'description':'Oxygen concentration',
        'lb':0,
        'ub':400,
        'interval':180,
    },
    {
        'dbtag':'T_optode',
        'unit':'Deg.C',
        'description':'Water temperature (optode)',
        'lb':-10,
        'ub':50,
        'interval':180,
    },
    {
        'dbtag':'AirSat',
        'unit':'%',
        'description':'Air saturation',
        'lb':0,
        'ub':130,
        'interval':180,
    },
    {
        'dbtag':'EC',
        'unit':'mS/cm',
        'description':'Electrical Conductivity',
        'lb':0,
        'interval':180,
    },
    {
        'dbtag':'T_ec',
        'unit':'Deg.C',
        'description':'Water temperature (conductivity probe)',
        'lb':-10,
        'ub':50,
        'interval':180,
    },
    {
        'dbtag':'sal',
        'unit':'PSU',
        'description':'Salinity',
        'lb':0,
        'interval':180,
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
