# -*- coding: utf-8 -*-
#tag = 'node-001'
name = 'CTD + optode'
location = 'Triple Mākāhā b'
note = 'Aanderaa 4330f + MS5803-14BA + EZO EC + BMP180'

log_dir = './log'
plot_dir = '../www'

plot_range = 24*7
data_source = '/home/nuc/node/www/poh/storage/sensor_data.db'

xbee_port = '/dev/ttyO1'
xbee_baud = 115200
optode_port = '/dev/ttyO2'

wait = 591

multi_sample = 7


conf = [
    {
        'dbtag':'Timestamp',
        'description':'Time of sampling',
        'plot':False,
    },
    {
        'dbtag':'P_180',
        'unit':'Pa',
        'description':'Barometric pressure (BMP180)',
        'plot':True,
        'lb':80e3,
        'ub':110e3,
        #'convf':lambda (x): x/1e3,
        #'convunit':'kPa',
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
        'description':'Water Temperature (MS5803-14BA)',
        'lb':-10,
        'ub':60,
    },
    {
        'dbtag':'ec',
        'unit':'uS/cm',
        'description':'Conductivity (EZO EC)',
        'plot':False,
        'lb':0,
        'ub':55e3,
    },
    {
        'dbtag':'sal',
        'unit':'(ppt)',
        'description':'Salinity (EZO EC)',
        'plot':False,
        'lb':0,
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
        'lb':-10,
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
    
