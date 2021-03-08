# -*- coding: utf-8 -*-
name = '"Constanze"'
location = '"Room 101"'
note = 'Experimental XBee 8x TSYS01'

conf = [
    {
        'dbtag':'idx',
        'description':'Sample Number',
        'unit':'-',
        'lb':24*3600/(16*8),
        'plot_range':7*24,
        'interval':16*8,
    },
    {
        'dbtag':'t1',
        'description':'Temperature',
        'unit':'Deg.C',
        'lb':0,
        'ub':40,
        'plot_range':7*24,
        'interval':16*8,
    },
    {
        'dbtag':'t3',
        'description':'Temperature',
        'unit':'Deg.C',
        'lb':0,
        'ub':40,
        'plot_range':7*24,
        'interval':16*8,
    },
    {
        'dbtag':'t5',
        'description':'Temperature',
        'unit':'Deg.C',
        'lb':0,
        'ub':40,
        'plot_range':7*24,
        'interval':16*8,
    },
    {
        'dbtag':'t7',
        'description':'Temperature',
        'unit':'Deg.C',
        'lb':0,
        'ub':40,
        'plot_range':7*24,
        'interval':16*8,
    },
    {
        'dbtag':'t9',
        'description':'Temperature',
        'unit':'Deg.C',
        'lb':0,
        'ub':40,
        'plot_range':7*24,
        'interval':16*8,
    },
    {
        'dbtag':'t11',
        'description':'Temperature',
        'unit':'Deg.C',
        'lb':0,
        'ub':40,
        'plot_range':7*24,
        'interval':16*8,
    },
    {
        'dbtag':'t13',
        'description':'Temperature',
        'unit':'Deg.C',
        'lb':0,
        'ub':40,
        'plot_range':7*24,
        'interval':16*8,
    },
    {
        'dbtag':'t15',
        'description':'Temperature',
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
        'description':'Solar panel voltage (after rectifier)',
        'lb':0,
        'ub':7,
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
