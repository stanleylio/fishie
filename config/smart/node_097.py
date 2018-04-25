# -*- coding: utf-8 -*-
name = 'Manoa Stream (Kanewai) Water Level'
location = 'Manoa Stream (Kanewai)'
google_earth_link = '#'
note = 'Ultrasonic tide gauge (XBee). One measurement every ~3 minutes. No RTC, no storage, telemetry only. Firmware us10c, hardware v4.2.'


conf = [
    {
        'dbtag':'d2w',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'lb':301,
        'ub':4999,
        'interval':180,
    },
    {
        'dbtag':'VbattV',
        'unit':'V',
        'description':'Battery voltage (Vbatt)',
        'lb':3.0,
        'interval':180,
    },
    {
        'dbtag':'ticker',
        'description':'1Hz ticker',
        'lb':0,
        'interval':180,
        'plot':False,
    },
    {   # had ticker when running us10b. later changed to us10c and ticker was replaced with idx.
        'dbtag':'idx',
        'description':'Sample index',
        'lb':0,
        'interval':180,
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
