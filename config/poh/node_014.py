name = 'Water Level (Wai 1)'
location = 'River Mākāhā'
google_earth_link = 'https://goo.gl/maps/ha2pmE8hEir'
note = 'Ultrasonic tide gauge (XBee). 1Hz measurements. Each transmission is average of 60 measurements. Firmware us14, hardware v5.3. Redeployed 20201202.'
latitude = 21.439750
longitude = -157.809800


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
        'lb':0,
        'ub':4.3,
        'interval':60,
    },
    {
        'dbtag':'Vs',
        'unit':'V',
        'description':'Solar panel voltage',
        'lb':0,
        'ub':7.0,
        'interval':60,
    },
    {
        'dbtag':'idx',
        'description':'Sample index',
        'lb':24*60,
        'interval':60,
    },
    {
        'dbtag':'sc',
        'description':'Sample Size (after rejecting invalid measurements)',
        'lb':48,
        'interval':60,
    },
    {
        'dbtag':'std',
        'unit':'mm',
        'description':'Sample standard deviation',
        #'lb':?,
        #'ub':?,
        'interval':60,
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
