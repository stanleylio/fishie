# -*- coding: utf-8 -*-
name = 'Water Level (DeBordieu Colony)'
location = 'DeBordieu Colony'
note = 'Ultrasonic tide gauge (cellular; 0.3~5m). Hardware v0.5.'
#latitude = 21.28851
#longitude = 157.80540

coreid = '240046000647363334373734'

INTERVAL_S = 2*6*60

conf = [
    {
        'dbtag':'ts',
        'description':'Sample time (Device clock)',
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'d2w',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'lb':301,
        'ub':4999,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'std',
        'unit':'mm',
        'description':'Sample standard deviation',
        #'lb':?,
        #'ub':?,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'Vb',
        'unit':'V',
        'description':'Battery voltage',
        'lb':3.7,
        'ub':4.2,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'SoC',
        'unit':'%',
        'description':'State of Charge',
        'lb':40,    # more like a warning than a valid range check
        'ub':100,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'sc',
        'description':'# of measurements within 3\u03c3',
        'lb':91,
        'ub':181,
        'interval':INTERVAL_S,
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
