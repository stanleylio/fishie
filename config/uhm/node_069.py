# -*- coding: utf-8 -*-
name = "Moli'i cellular Water Level"
location = "Moli'i"
note = 'Cellular ultrasonic tide gauge. Firmware p5b, hardware v0.2. 1 measurement per second; 1 sample = average of 60 measurements; 10 samples per transmission.'
google_earth_link = 'https://goo.gl/maps/C7bPidpD5Km'

coreid = '4d0057001851353338363036'


conf = [
    {
        'dbtag':'Timestamp',
        'description':'Sample time (device clock)',
    },
    {
        'dbtag':'d2w',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'lb':300,
        'ub':5000,
    },
    {
        'dbtag':'VbattV',
        'unit':'V',
        'description':'Battery voltage',
        'lb':3.7,
        'ub':5.5,
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf,basename(__file__).split('.')[0].replace('_','-'))
