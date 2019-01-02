# -*- coding: utf-8 -*-
name = '"Komorebi"'
location = 'Staging Bay, Flyover State'
note = 'Ultrasonic tide gauge (XBee). 1Hz measurements. Each transmission is average of 60 measurements. Firmware us13a, hardware v5.3.'


conf = [
    {
        'dbtag':'d2w',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'lb':301,
        'ub':4999,
        'interval':60,
    },
    {
        'dbtag':'Vb',
        'unit':'V',
        'description':'Battery voltage',
        'lb':0,
        'ub':4.3,
        'interval':60,
    },
    {
        'dbtag':'Vs',
        'unit':'V',
        'description':'Solar panel voltage',
        'lb':0,
        'ub':6,
        'interval':60,
    },
    {
        'dbtag':'idx',
        'description':'Sample index',
        'lb':0,
        'interval':60,
    },
    {
        'dbtag':'sc',
        'description':'Sample Size (after rejecting invalid measurements)',
        'lb':48,
        'interval':60,
    },
    {
        'dbtag':'c',
        'description':'Internal 1Hz counter',
        'lb':24*3600,
        'interval':60,
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
