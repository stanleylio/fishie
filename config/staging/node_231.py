# -*- coding: utf-8 -*-
name = '"Sprezzatura"'
location = '"Per aspera ad astra"'
note = 'Ultrasonic tide gauge (cellular; 0.3~5.0 meter). Each sample is average of N_AVG measurements taken every second. Hardware v1.0.'

coreid = 'e00fce685f4afafdcde95e75'

conf = [
    {
        'dbtag':'ts',
        'description':'Sample time (Device clock)',
        'interval':15*60,
    },
    {
        'dbtag':'d2w',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'lb':301,
        'ub':4999,
        'interval':15*60,
    },
    {
        'dbtag':'Vb',
        'unit':'V',
        'description':'Battery voltage',
        'lb':3.7,
        'ub':5.5,
        'interval':15*60,
    },
    {
        'dbtag':'SoC',
        'unit':'%',
        'description':'State of Charge',
        'lb':40,    # more like a warning than a valid range check
        'ub':100,
        'interval':15*60,
    },
    {
        'dbtag':'std',
        'description':'Sample standard deviation',
        'lb':0,
        #'ub':?,
        'interval':15*60,
    },
    {
        'dbtag':'sc',
        'description':'Sample count',
        'lb':0,
        'ub':181,
        'interval':15*60,
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
