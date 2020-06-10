name = 'Chris\' (Wai‘ōma‘o Stream)'
location = 'Wai‘ōma‘o Stream, Palolo Valley'
note = 'Ultrasonic tide gauge measuring distance to water surface from fixed structure. One measurement per second, one transmission (average of past minute) per minute. Hardware v4.2, firmware us10b. (low-cost charger, welded battery tabs)'
latitude = 21.3034
longitude = -157.7855

conf = [
    {
        'dbtag':'d2w',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'lb':301,
        'ub':4999,
        'interval':180,
    },
    {
        'dbtag':'Vsolar',
        'unit':'V',
        'description':'Solar panel voltage',
        'lb':0,
        'ub':5.5,
        'interval':180,
    },
    {
        'dbtag':'idx',
        'description':'Sample index',
        'lb':0,
        'interval':180,
    },
    {   # deprecated after upgrading to firmware us11b on hardware 5.0
        'dbtag':'VbattV',
        'unit':'V',
        'description':'Battery voltage',
        'lb':2.7,
        'interval':60,
        'plot':False,
    },
    {   # deprecated
        'dbtag':'ticker',
        'description':'Monotonic increasing 1Hz ticker',
        'lb':0,
        'interval':60,
        'plot':False,
    },
    {   # deprecated
        'dbtag':'sample_size',
        'description':'Number of valid readings in the 60 measurements',
        'lb':0,
        'ub':60,
        'interval':60,
        'plot':False,
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
    create_table(conf, basename(__file__).split('.')[0].replace('_', '-'))
