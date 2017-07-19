# -*- coding: utf-8 -*-
name = 'Water Level'
location = 'Coconut Island'
note = 'Ultrasonic tide gauge (HW v4.2, FW: us10)'


conf = [
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
        'description':'Battery voltage (Vbatt)',
        'lb':2.4,
    },
    {
        'dbtag':'ticker',
        'description':'1Hz ticker',
        'lb':0,
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
