# -*- coding: utf-8 -*-
name = 'Ala Moana buoy SeapHOx + CTD'
location = 'Ala Moana buoy'
note = 'SeapHOx + CTD 02026'

#coreid = '5d003e001951353338363036'
coreid = '23003b000351353337353037'

conf = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE NOT NULL',
        'description':'Sensor clock (POSIX)',
        'plot':True,
        'interval':6*60,
    },
    {
        'dbtag':'idx',
        'description':'Sample Number',
        'unit':'-',
        'lb':0,
        'plot_range':7*24,
        'interval':6*60,
    },
    {
        'dbtag':'tC',
        'description':'Temperature',
        'unit':'Deg.C',
        'lb':0,
        'ub':40,
        'plot_range':7*24,
        'interval':6*60,
    },
    {
        'dbtag':'epH',
        'description':'External pH',
        'unit':'-',
        'lb':7,
        'ub':11,
        'plot_range':7*24,
        'interval':6*60,
    },
    {
        'dbtag':'ipH',
        'description':'Internal pH',
        'unit':'-',
        'lb':7,
        'ub':11,
        'plot_range':7*24,
        'interval':6*60,
    },
    {
        'dbtag':'pHC',
        'description':'pH Temperature',
        'unit':'Deg.C',
        'lb':0,
        'ub':40,
        'plot_range':7*24,
        'interval':6*60,
    },
    {
        'dbtag':'dbar',
        'description':'Pressure',
        'unit':'dbar',
        'lb':0,
        'ub':100,
        'plot_range':7*24,
        'interval':6*60,
    },
    {
        'dbtag':'psu',
        'description':'Salinity',
        'unit':'PSU',
        'lb':25,
        'ub':35,
        'plot_range':7*24,
        'interval':6*60,
    },
    {
        'dbtag':'ec_S_m',
        'description':'Conductivity',
        'unit':'S/m',
        'lb':0,
        'ub':100,
        'plot_range':7*24,
        'interval':6*60,
    },
    {
        'dbtag':'o2_mg_L',
        'description':'Oxygen',
        'unit':'mg/L',
        'lb':0,
        'ub':10,
        'plot_range':7*24,
        'interval':6*60,
    },
    {
        'dbtag':'rh',
        'description':'Relative Humidity (internal)',
        'unit':'%',
        'lb':0,
        'ub':50,
        'plot_range':7*24,
        'interval':6*60,
    },
    {
        'dbtag':'iC',
        'description':'Internal Temperature',
        'unit':'Deg.C',
        'lb':0,
        'ub':40,
        'plot_range':7*24,
        'interval':6*60,
    },
    {
        'dbtag':'Vb',
        'unit':'V',
        'description':'Battery voltage (telemetry relay\'s)',
        'lb':3.7,
        'ub':5.5,
        'interval':12*60,
    },
    {
        'dbtag':'SoC',
        'unit':'%',
        'description':'State of Charge (telemetry relay\'s)',
        'lb':30,
        'ub':100,
        'interval':12*60,
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
