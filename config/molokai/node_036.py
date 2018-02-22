# -*- coding: utf-8 -*-
name = 'Ali`i Water Level'
location = 'Ali`i Fishpond, Molokaʻi (21.073033, -156.981083)'
google_earth_link = 'https://goo.gl/maps/FTXJBZtAAhH2'
note = 'Ultrasonic tide gauge (XBee). Each sample is the sample mean of 60 measurements taken every second (excluding any out-of-range ones). Firmware us10b, hardware v4.2.'


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
        'lb':2.8,
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
        for k,v in c.iteritems():
            print(k,':',v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf,basename(__file__).split('.')[0].replace('_','-'))
