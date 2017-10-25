# -*- coding: utf-8 -*-
name = '(TBD)'
location = '(TBD)'
note = 'Cellular ultrasonic tide gauge. Each sample is average of 60 measurements taken every second. One transmission every 10 samples. Firmware p5d, hardware v0.2.'

coreid = '4d0038001751353338363036'


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
    {
        'dbtag':'SoC',
        'unit':'%',
        'description':'State of Charge',
        'lb':0,
        'ub':100,
    },
]


if '__main__' == __name__:
    for c in conf:
        print('- - -')
        for k,v in c.iteritems():
            print(k,':',v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf,basename(__file__).split('.')[0].replace('_','-'))
