# -*- coding: utf-8 -*-
name = 'Water Depth (pending deployment)'
location = 'Mākāhā X'
note = 'Ultrasonic tide gauge. One distance-to-water-surface measurement per second; each sample is the sample mean of 60 measurements. RTC and local storage enabled.'


conf = [
    {
        'dbtag':'ts',
        'description':'Device time',
        'plot':False,
        'lb':0,
    },
    {
        'dbtag':'d2w',
        'unit':'mm',
        'description':'Distance from sensor to water surface (sample mean)',
        'lb':300,
        'ub':5000,
    },
    {
        'dbtag':'VbattV',
        'unit':'V',
        'description':'Battery voltage',
        'lb':2.4,
    },
    {
        'dbtag':'ticker',
        'description':'Message ID',
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
