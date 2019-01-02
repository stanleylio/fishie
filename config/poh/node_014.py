# -*- coding: utf-8 -*-
name = 'Wai 1 Water Level'
location = 'River Mākāhā'
google_earth_link = 'https://goo.gl/maps/ha2pmE8hEir'
note = 'Ultrasonic tide gauge (1st gen PCB)'
latitude = 21.439750
longitude = -157.809800


conf = [
    {
        'dbtag':'d2w',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'lb':301,
        'ub':4999,
        'interval':400,
    },
    {
        'dbtag':'VbattV',
        'unit':'V',
        'description':'Battery voltage (Vbatt)',
        'lb':3.0,
        'interval':400,
    },
    {
        'dbtag':'ticker',
        'description':'1Hz ticker',
        'lb':0,
        'interval':400,
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
