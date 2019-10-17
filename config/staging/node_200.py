# -*- coding: utf-8 -*-
name = '"Knack II"'
location = '(TBD)'
note = 'Ultrasonic tide gauge (cellular; 10m version). Each sample is average of 60 measurements taken every second. One transmission every 10 samples. Firmware p6d, hardware v0.4.'

coreid = '350020001047373334363431'

conf = [
    {
        'dbtag':'Timestamp',
        'description':'Sample time (Electron clock)',
        'interval':10*60,
    },
    {
        'dbtag':'d2w',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'lb':301,
        'ub':9998,
        'interval':10*60,
    },
    {
        'dbtag':'VbattV',
        'unit':'V',
        'description':'Battery voltage',
        'lb':3.7,
        'ub':5.5,
        'interval':10*60,
    },
    {
        'dbtag':'SoC',
        'unit':'%',
        'description':'State of Charge',
        'lb':40,    # more like a warning than a valid range check
        'ub':100,
        'interval':10*60,
    },
    {
        'dbtag':'sample_size',
        'description':'Number of valid readings in the 60 measurements',
        'lb':0,
        'ub':60,
        'interval':10*60,
    },
]


if '__main__' == __name__:
    for c in conf:
        print('- - -')
        for k, v in c.items():
            print(k, ':' ,v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf, basename(__file__).split('.')[0].replace('_', '-'))
