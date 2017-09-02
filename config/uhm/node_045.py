# -*- coding: utf-8 -*-
name = '(TBD)'
location = 'UH Manoa'
note = 'Cellular ultrasonic tide gauge'

coreid = '280021001951353338363036'


conf = [
    {
        'dbtag':'Timestamp',
        'description':'Sample time (Electron clock)',
        'plot':True,
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
