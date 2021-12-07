name = 'Kim\'s'
location = 'TNC'
google_earth_link = '#'
note = 'Ultrasonic tide gauge (cellular; 0.5~10m). Hardware v0.6.'
latitude = 21.431470
longitude = -157.81703
coreid = '550040000251383133363636'

INTERVAL_S = 2*6*60

conf = [
    {
        'dbtag':'ts',
        'description':'Sample time (device clock)',
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
        'ub':5.5,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'SoC',
        'unit':'%',
        'description':'State of Charge',
        'lb':40,
        'ub':100,
        'interval':10*INTERVAL_S,
        'plot':False,
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
            print(k, ':', v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf,basename(__file__).split('.')[0].replace('_', '-'))
