# -*- coding: utf-8 -*-
name = 'Pua Pond Optode'
location = 'Pua Pond, Paepae O He`eia Fishpond'
note = 'Aanderaa oxygen optode 4531. Hardware v5.4, firmware aa1.'
latitude = 21.439722
longitude = -157.809722

conf = [
    {
        'dbtag':'sn',
        'unit':'-',
        'description':'Sensor serial number',
        'interval':5*60,
    },
    {
        'dbtag':'O2',
        'unit':'uM',
        'description':'Dissolved oxygen',
        'lb':100,
        'ub':300,
        'interval':5*60,
    },
    {
        'dbtag':'air',
        'unit':'%',
        'description':'Air saturation',
        'lb':50,
        'interval':5*60,
    },
    {
        'dbtag':'Tw',
        'unit':'Deg.C',
        'description':'Water temperature',
        'lb':-5,
        'ub':40,
        'interval':5*60,
    },
    {
        'dbtag':'Vb',
        'description':'Battery voltage',
        'lb':3.0,
        'ub':4.3,
        'interval':5*60,
    },
    {
        'dbtag':'Vs',
        'description':'Solar panel voltage (after rectifier)',
        'lb':0,
        'ub':7.5,
        'interval':5*60,
    },
    {
        'dbtag':'idx',
        'description':'Sample index',
        'lb':24*60*60/(5*60),
        'interval':5*60,
    },
    {
        'dbtag':'c',
        'description':'1Hz ticker',
        'lb':24*60*60,
        'interval':5*60,
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
