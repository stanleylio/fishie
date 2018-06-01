# -*- coding: utf-8 -*-
name = '(TBD)'
location = '(TBD)'
note = 'Cellular ultrasonic tide gauge. One measurement per minute, one transmission every 10 measurements. Firmware p5f, hardware v0.2 (with US_EN patch).'

coreid = '290047000347363334383136'


conf = [
    {
        'dbtag':'Timestamp',
        'description':'Sample time (device clock)',
        'interval':10*60,
    },
    {
        'dbtag':'d2w',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'lb':300,
        'ub':4999,
        'interval':10*60,
    },
    {
        'dbtag':'VbattV',
        'unit':'V',
        'description':'Battery voltage',
        'lb':3.4,
        'ub':5.5,
        'interval':10*60,
    },
    {
        'dbtag':'SoC',
        'unit':'%',
        'description':'State of Charge',
        'lb':30,    # more like a warning than a valid range check
        'ub':100,
        'interval':10*60,
    },
    {
        'dbtag':'sample_size',
        'description':'Number of valid readings in set of measurements',
        'lb':0,
        'ub':60,
        'interval':10*60,
        'plot':False,
    },
]


if '__main__' == __name__:
    for c in conf:
        print('- - -')
        for k,v in c.items():
            print(k, ':', v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf, basename(__file__).split('.')[0].replace('_', '-'))
