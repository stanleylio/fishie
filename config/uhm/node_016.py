# -*- coding: utf-8 -*-
name = 'Manoa Stream Water Level'
location = 'Manoa Stream, UH Manoa'
note = 'Ultrasonic tide gauge (Particle Electron)'

coreid = '1f0024001751353338363036'


conf = [
    {
        'dbtag':'d2w',
        'dbtype':'DOUBLE',
        'comtag':'d2w',
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
    from storage.storage2 import create_table

    conf.insert(0,{'dbtag':'ReceptionTime','dbtype':'DOUBLE NOT NULL'})

    create_table(conf,'node-016')
