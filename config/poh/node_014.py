# -*- coding: utf-8 -*-
name = 'River Mākāhā Water Level'
location = 'River Mākāhā'
note = 'Ultrasonic tide gauge (1st gen PCB)'


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
    {
        'dbtag':'VbattV',
        'dbtype':'DOUBLE',
        'comtag':'VbattV',
        'unit':'V',
        'description':'Battery voltage (Vbatt)',
        'lb':2400,
    },
    {
        'dbtag':'ticker',
        'dbtype':'DOUBLE',
        'comtag':'ticker',
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
    from storage.storage2 import create_table

    conf.insert(0,{'dbtag':'ReceptionTime','dbtype':'DOUBLE NOT NULL'})

    create_table(conf,'node-014')
