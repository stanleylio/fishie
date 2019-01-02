# -*- coding: utf-8 -*-
name = 'Hīhīmanu Water Level'
location = 'Hīhīmanu (first mākāhā)'
google_earth_link = 'https://goo.gl/maps/eY752oYMdV42'
note = 'Cellular ultrasonic tide gauge. Each sample is average of 60 measurements taken every second. One transmission every 10 samples. Firmware p5e, hardware v0.2 (with US_EN patch).'
latitude = 21.433967
longitude = -157.805333

coreid = '3e0042001951353338363036'


conf = [
    {
        'dbtag':'Timestamp',
        'description':'Sample time (Electron clock)',
        'interval':10*60,
    },
    {
        'dbtag':'d2w',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'lb':301,
        'ub':4999,
        'interval':10*60,
    },
    {
        'dbtag':'VbattV',
        'unit':'V',
        'description':'Battery voltage',
        'lb':3.7,
        'ub':5.5,
        'interval':10*60,
    },
    {
        'dbtag':'SoC',
        'unit':'%',
        'description':'State of Charge',
        'lb':30,    # more like a warning than a valid range check
        'ub':100,
        'interval':10*60,
    },
    {
        'dbtag':'sample_size',
        'description':'Number of valid readings in the 60 measurements',
        'lb':0,
        'ub':60,
        'interval':10*60,
    },
]


if '__main__' == __name__:
    for c in conf:
        print('- - -')
        for k, v in c.items():
            print(k, ':' ,v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf, basename(__file__).split('.')[0].replace('_', '-'))
