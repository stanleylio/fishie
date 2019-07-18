# -*- coding: utf-8 -*-
name = '(decommissioned)'
location = 'Mokauea Island'
note = 'Dual temperature probes (surface + bottom)'
latitude = 21.307778
longitude = -157.891389

conf = [
    {
        'dbtag':'idx',
        'description':'Sample Number',
        'unit':'-',
        'lb':0,
        'plot_range':7*24,
        'interval':16*8,
    },
    {
        'dbtag':'t0',
        'description':'Surface temperature (0x76)',
        'unit':'Deg.C',
        'lb':0,
        'ub':40,
        'plot_range':7*24,
        'interval':16*8,
    },
    {
        'dbtag':'t1',
        'description':'Bottom temperature (0x77)',
        'unit':'Deg.C',
        'lb':0,
        'ub':40,
        'plot_range':7*24,
        'interval':16*8,
    },
    {
        'dbtag':'Vb',
        'unit':'V',
        'description':'Battery voltage',
        'lb':3.0,
        'ub':4.2,
        'interval':16*8,
    },
    {
        'dbtag':'Vs',
        'unit':'V',
        'description':'Solar panel voltage',
        'lb':0,
        'ub':7.5,
        'interval':16*8,
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
