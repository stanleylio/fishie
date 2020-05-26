name = 'Water Level (Barnstable Harbor)'
location = 'Barnstable Harbor'
note = 'Ultrasonic tide gauge (cellular; 0.5~10m). Hardware v0.5.'
latitude = 41.706183
longitude = -70.298800

coreid = '3a0038001751353338363036'

conf = [
    {
        'dbtag':'ts',
        'description':'Sample time (Device clock)',
        'interval':2*6*60,
    },
    {
        'dbtag':'d2w',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'lb':501,
        'ub':9998,
        'interval':2*6*60,
    },
    {
        'dbtag':'std',
        'unit':'mm',
        'description':'Sample standard deviation',
        'lb':0,
        'interval':2*6*60,
    },
    {
        'dbtag':'Vb',
        'unit':'V',
        'description':'Battery voltage',
        'lb':3.7,
        'ub':4.2,
        'interval':2*6*60,
    },
    {
        'dbtag':'SoC',
        'unit':'%',
        'description':'State of Charge',
        'lb':40,    # more like a warning than a valid range check
        'ub':100,
        'interval':2*6*60,
    },
    {
        'dbtag':'sc',
        'description':'# of measurements within 3\u03c3',
        'lb':91,
        'ub':181,
        'interval':2*6*60,
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
