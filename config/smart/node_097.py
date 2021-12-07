name = 'Manoa Stream (Kanewai) Water Level'
location = 'Manoa Stream (Kanewai)'
google_earth_link = '#'
note = 'Ultrasonic tide gauge (XBee). v5 hardware; us14 firmware.'
latitude = 21.29527
longitude = -157.81317

conf = [
    {
        'dbtag':'d2w',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'lb':301,
        'ub':4999,
        'interval':60,
    },
    {
        'dbtag':'Vb',
        'unit':'V',
        'description':'Battery voltage',
        'lb':3.0,
        'interval':60,
    },
    {
        'dbtag':'Vs',
        'unit':'V',
        'description':'Solar panel voltage',
        'ub':7.0,
        'interval':60,
    },
    {
        'dbtag':'std',
        'description':'Standard Deviation (after rejecting invalid measurements)',
        'interval':60,
    },
    {
        'dbtag':'sc',
        'description':'Sample Size (after rejecting invalid measurements)',
        'lb':0,
        'interval':60,
    },
    {
        'dbtag':'ticker',
        'description':'1Hz ticker',
        'lb':0,
        'interval':60,
        'plot':False,
    },
    {   # had ticker when running us10b. later changed to us10c and ticker was replaced with idx.
        'dbtag':'idx',
        'description':'Sample index',
        'lb':0,
        'interval':60,
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
