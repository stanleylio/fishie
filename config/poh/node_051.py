name = 'Water Level (Mākāhā Nui)'
location = 'Mākāhā Nui ("Storm Mākāhā")'
google_earth_link = 'https://goo.gl/maps/74uCxGwoAJB2'
note = 'Cellular ultrasonic tide gauge. Each sample is average of 60 measurements taken every second. One transmission every 10 samples. v0.6 board. Replaced 20201112.'
latitude = 21.437250
longitude = -157.805850

coreid = '3e00580006504b3842323220'

INTERVAL_S = 2*6*60

conf = [
    {
        'dbtag':'ts',
        'description':'Sample time (Electron clock)',
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
    },
    {
        'dbtag':'sc',
        'description':'Number of valid readings in the 60 measurements',
        'lb':90,
        'ub':181,
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
