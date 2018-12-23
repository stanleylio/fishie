# -*- coding: utf-8 -*-
name = 'FLNTUSB (staging)'
location = '(TBD)'
note = 'FLNTUSB, chlorophyll and turbidity (XBee FLNTUSB 5101)'

conf = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE NOT NULL',
        'description':'Sensor clock (POSIX)',
        'plot':True,
        'interval':12*60,
    },
    {
        'dbtag':'C',
        'description':'Chlorophyll (EX/EM: 470/695nm)',
        'unit':'ug/L',
        'lb':0,
        'ub':0.0121*(4130 - 48),
        'plot_range':7*24,
        'interval':12*60,
    },
    {
        'dbtag':'N',
        'description':'Turbidity (700nm)',
        'unit':'NTU',
        'lb':0,
        'ub':0.0060*(4130 - 43),
        'plot_range':7*24,
        'interval':12*60,
    },
    {
        'dbtag':'ch695',
        'description':'Chlorophyll raw count (695nm)',
        'unit':'-',
        'lb':0,
        'ub':4130,
        'plot_range':7*24,
        'interval':12*60,
    },
    {
        'dbtag':'ch700',
        'description':'Turbidity raw count (700nm)',
        'unit':'-',
        'lb':0,
        'ub':4130,
        'plot_range':7*24,
        'interval':12*60,
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
        'dbtag':'Vs',
        'unit':'V',
        'description':'Solar input voltage (telemetry relay\'s)',
        'lb':0,
        'ub':6,
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
