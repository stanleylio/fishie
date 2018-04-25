# -*- coding: utf-8 -*-
name = 'Stream Water Level'
location = '(TBD)'
google_earth_link = '#'
note = 'Ultrasonic tide gauge (XBee). One measurement every ~3 minutes. Firmware us11b, hardware v5.0.'


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
        'dbtag':'Vsolar',
        'unit':'V',
        'description':'Solar panel voltage',
        'lb':0,
        'ub':5.5,
        'interval':60,
    },
    {
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
            print(k,':',v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf,basename(__file__).split('.')[0].replace('_','-'))
