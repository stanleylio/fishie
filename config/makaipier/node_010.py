# -*- coding: utf-8 -*-
name = 'Water Level'
location = 'Makai Research Pier'
note = 'Ultrasonic tide gauge measuring distance to water surface from fixed structure. One measurement per second, one transmission (average of past minute) per minute. Hardware v4.2, firmware us10b.'


conf = [
    {
        'dbtag':'d2w',
        'unit':'mm',
        'description':'Distance from base of sensor to water surface',
        'lb':300,
        'ub':4999,
    },
    {
        'dbtag':'VbattV',
        'unit':'V',
        'description':'Battery voltage',
        'lb':2.5,
    },
    {
        'dbtag':'ticker',
        'description':'Monotonic increasing 1Hz ticker',
        'lb':0,
    },
    {
        'dbtag':'sample_size',
        'description':'Number of valid readings in the 60 measurements',
        'lb':0,
        'ub':60,
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
