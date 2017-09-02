# -*- coding: utf-8 -*-
name = 'Storm Mākāhā Water Level'
location = 'Storm Mākāhā'
note = 'Firmware p5b, hardware v0.2. 1 measurement per second; 1 sample = average of 60 measurements; 10 samples per transmission.'

coreid = '230053001951353338363036'


conf = [
    {
        'dbtag':'Timestamp',
        'description':'Sample time (Electron clock)',
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
