name = 'Water Level'
location = 'Marine Corps Base Hawaii'
note = 'Ultrasonic tide gauge (cellular; 0.3~5m). v0.6 board.'
latitude = 21.434098
longitude = -157.757516
deployment_status = 'deployed'

coreid = '350020001047373334363431'

INTERVAL_S = 10*60

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
        'ub':4.2,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'SoC',
        'unit':'%',
        'description':'State of Charge',
        'lb':40,    # more like a warning than a valid range check
        'ub':100,
        'interval':10*INTERVAL_S,
        'plot':False,
    },
    {
        'dbtag':'sc',
        'description':'Number of valid readings in the 60 measurements',
        'lb':30,
        'ub':60,
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
