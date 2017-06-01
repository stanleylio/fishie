# -*- coding: utf-8 -*-
name = '(Experimental)'
location = 'Manoa Stream, UH Manoa'
note = 'Ultrasonic tide gauge (Particle Electron)'

coreid = '280021001951353338363036'


conf = [
    {
        'dbtag':'d2w',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'lb':300,
        'ub':5000,
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