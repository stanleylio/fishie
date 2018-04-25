# -*- coding: utf-8 -*-
name = 'Manoa Stream (UH) Water Level'
location = 'Manoa Stream (Japanese Garden, UHM)'
google_earth_link = '#'
note = 'Ultrasonic tide gauge (XBee). Each sample is the sample mean of 60 measurements taken every second (excluding any out-of-range ones). Firmware us10c, hardware v5.0.'


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
        'dbtag':'Vcc',
        'unit':'V',
        'description':'µC supply voltage',
        'lb':2.7,
        'ub':3.6,
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
        'dbtag':'ticker',
        'description':'1Hz ticker',
        'lb':0,
        'interval':60,
    },
    {
        'dbtag':'sample_size',
        'description':'# of valid measurements in the psat 60',
        'lb':1,
        'ub':60,
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
