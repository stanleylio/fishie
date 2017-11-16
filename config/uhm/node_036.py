# -*- coding: utf-8 -*-
name = '(TBD)'
location = 'Somewhere on Molokaʻi'
google_earth_link = '#'
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
        'lb':2.7,
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
        'description':'# of valid measurements in the past 60 measurements',
        'lb':0,
        'ub':60,
        'interval':10*60,
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
