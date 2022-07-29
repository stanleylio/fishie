name = '"Next-to-NOAA"'
location = 'Kāneʻohe Bay, Oahu, Hawaii'
google_earth_link = 'https://goo.gl/maps/QWuNSn4Ge9m'
note = 'Cellular ultrasonic tide gauge. Each sample is average of 60 measurements taken every second. One transmission every 10 samples. Firmware p5e, hardware v0.2.'
latitude = 21.433037
longitude = -157.789814
deployment_status = 'deployed'

#coreid = '1c0038001647373037383634'
coreid = '49005a0006504b3842323220'

INTERVAL_S = 9*60

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
        'lb':300,
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
        'lb':40,
        'ub':100,
        'interval':INTERVAL_S,
        'plot': False,
    },
    {
        'dbtag':'sc',
        'description':'Number of valid readings in the 60 measurements',
        'lb':0,
        'ub':60,
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
    create_table(conf, basename(__file__).split('.')[0].replace('_', '-'))
