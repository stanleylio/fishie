# -*- coding: utf-8 -*-
name = 'Hīhīmanu Oxygen and Depth'
location = 'Hīhīmanu (first mākāhā)'
note = 'Beaglebone-based node measuring oxygen, temperature and water depth'

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
        'dbtag':'Timestamp',
        'dbtype':'DOUBLE NOT NULL',
        'description':'Time of sampling',
        'plot':False,
    },
    {
        'dbtag':'P_180',
        'unit':'Pa',
        'description':'Barometric pressure (BMP180)',
        'lb':90e3,
        'ub':110e3,
    },
    {
        'dbtag':'T_180',
        'unit':'Deg.C',
        'description':'Enclosure temperature (BMP180)',
        'lb':-10,
        'ub':80,
    },
    {
        'dbtag':'P_5803',
        'unit':'kPa',
        'description':'Water pressure (MS5803-14BA)',
        'lb':80,
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
        'dbtag':'T_TSYS01',
        'unit':'Deg.C',
        'description':'Water temperature (TSYS01)',
        'plot':False,
        'lb':-10,
        'ub':50,
    },
    {
        'dbtag':'T_7051',
        'unit':'Deg.C',
        'description':'Water temperature (Si7051)',
        'plot':False,
        'lb':-10,
        'ub':50,
    },
    {
        'dbtag':'O2Concentration',
        'unit':'uM',
        'description':'Oxygen concentration (4330F)',
        'lb':0,
        'ub':450,
    },
    {
        'dbtag':'AirSaturation',
        'unit':'%',
        'description':'Air saturation (4330F)',
        'lb':0,
        'ub':150,
    },
    {
        'dbtag':'Temperature',
        'unit':'Deg.C',
        'description':'Water temperature (4330F)',
        'lb':-20,
        'ub':60,
    },
    {
        'dbtag':'CalPhase',
        'unit':'Deg',
        'description':'CalPhase',
        'plot':False,
    },
    {
        'dbtag':'TCPhase',
        'unit':'Deg',
        'description':'TCPhase',
        'plot':False,
    },
    {
        'dbtag':'C1RPh',
        'unit':'Deg',
        'description':'C1RPh',
        'plot':False,
    },
    {
        'dbtag':'C2RPh',
        'unit':'Deg',
        'description':'C2RPh',
        'plot':False,
    },
    {
        'dbtag':'C1Amp',
        'unit':'mV',
        'description':'C1Amp',
        'plot':False,
    },
    {
        'dbtag':'C2Amp',
        'unit':'mV',
        'description':'C2Amp',
        'plot':False,
    },
    {
        'dbtag':'RawTemp',
        'unit':'mV',
        'description':'RawTemp',
        'plot':False,
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

    import sys
    sys.path.append('../..')
    from storage.storage2 import create_table
    create_table(conf,__file__.split('.')[0].replace('_','-'))
    
