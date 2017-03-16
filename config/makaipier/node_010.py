# -*- coding: utf-8 -*-
name = 'Makai Pier Water Level'
location = 'Makai Research Pier'
note = 'Ultrasonic tide gauge (us3, but tagged as us5 by mistake)'


conf = [
    {
        'dbtag':'ReceptionTime',
        'dbtype':'DOUBLE NOT NULL',
        'description':'Time of reception at base station; POSIX timestamp.',
        'plot':False,
    },
    {
        'dbtag':'ticker',
        'dbtype':'DOUBLE',
        'description':'Broadcast sequence number',
        'plot':False,
        'lb':0,
    },
    {
        'dbtag':'d2w',
        'dbtype':'DOUBLE',
        'unit':'mm',
        'description':'Distance from base of sensor to water surface',
        'lb':300,
        'ub':5000,
    },
    {
        'dbtag':'Vbatt',
        'dbtype':'DOUBLE',
        'unit':'V',
        'description':'Battery voltage',
        'lb':2.5,
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
    create_table(conf,__file__.split('.')[0].replace('_','-'))
    
