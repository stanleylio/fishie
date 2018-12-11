# -*- coding: utf-8 -*-
name = 'Auwai (beach) Water Level'
location = 'Nomilo Fishpond, Kauaʻi, Hawai‘i (21.884722, -159.528333)'
#google_earth_link = '#'
note = 'Ultrasonic tide gauge (XBee). 1Hz measurements; each transmission is average of 60 measurements. Firmware us11c, hardware v5.0.'


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
        'dbtag':'Vs',
        'unit':'V',
        'description':'Solar panel voltage',
        'lb':0,
        'ub':5.5,
        'interval':180,
    },
    {
        'dbtag':'idx',
        'description':'Sample index',
        'lb':24*60,
        'interval':180,
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