# -*- coding: utf-8 -*-
tag = 'node-002'
name = 'Fish pan'
location = 'Mākāhā 1'
note = 'Aanderaa 4330f + MS5803-14BA + EZO EC + BMP180'

log_dir = './log'
plot_dir = '../www'

plot_range = 24*7

xbee_port = '/dev/ttyO1'
xbee_baud = 115200

optode_port = '/dev/ttyO2'

wait = 592
#wait = 0

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
        'description':'Barometric Pressure',
        'lb':80e3,
        'ub':110e3,
        #'convf':lambda (x): x/1e3,
        #'convunit':'kPa',
    },
    {
        'dbtag':'T_180',
        'unit':'Deg.C',
        'description':'Casing Temperature',
        'lb':-10,
        'ub':80,
    },
    {
        'dbtag':'P_5803',
        'unit':'kPa',
        'description':'Water Pressure',
        'lb':80,
        'ub':150,
    },
    {
        'dbtag':'T_5803',
        'unit':'Deg.C',
        'description':'Water Temperature (5803)',
        'lb':-10,
        'ub':60,
    },
    {
        'dbtag':'ec',
        'unit':'uS/cm',
        'description':'Conductivity',
        'lb':0,
        'ub':55e3,
    },
    {
        'dbtag':'sal',
        'unit':'(ppt)',
        'description':'Salinity',
        'plot':False,
        'lb':0,
    },
    {
        'dbtag':'O2Concentration',
        'unit':'uM',
        'description':'Oxygen Concentration',
        'lb':0,
        'ub':450,
    },
    {
        'dbtag':'AirSaturation',
        'unit':'%',
        'description':'Air Saturation',
        'lb':0,
        'ub':150,
    },
    {
        'dbtag':'Temperature',
        'unit':'Deg.C',
        'description':'Water Temperature (4330F)',
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
    
