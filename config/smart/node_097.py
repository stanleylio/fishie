# -*- coding: utf-8 -*-
name = 'Water Level'
location = '(TBD)'
note = 'Ultrasonic tide gauge (v4.2). One sample per minute. Each sample is the sample mean of the past 60 measurements taken at 1Hz. Telemetry only. No RTC.'


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
        'dbtag':'VbattV',
        'unit':'V',
        'description':'Battery voltage (Vbatt)',
        'lb':3.0,
        'interval':60,
    },
    {
        'dbtag':'ticker',
        'description':'1Hz ticker',
        'lb':0,
        'interval':60,
        'plot':False,
    },
    {   # had ticker when running us10b. later changed to us10c and ticker was replaced with idx.
        'dbtag':'idx',
        'description':'Sample index',
        'lb':0,
        'interval':60,
    },
]


if '__main__' == __name__:
    for c in conf:
        print('- - -')
        for k,v in c.items():
            print(k, ':', v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf, basename(__file__).split('.')[0].replace('_', '-'))
