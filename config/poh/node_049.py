name = 'Water Level (Hīhīmanu)'
location = 'Hīhīmanu (first mākāhā)'
google_earth_link = 'https://goo.gl/maps/eY752oYMdV42'
note = 'Cellular ultrasonic tide gauge. Hardware upgraded from v0.4 to v0.5 on 20200124. Firmware upgraded on 20210316.'
latitude = 21.433967
longitude = -157.805333

coreid = '3e0042001951353338363036'

# expected transmission interval in seconds
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
        'lb':0,
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
        'lb':30,    # more like a warning than a valid range check
        'ub':100,
        'interval':10*INTERVAL_S,   # this is transmitted with ~10% chance. not an important or reliable parameter.
    },
    {
        'dbtag':'sc',
        'description':'# of measurements within 3σ',
        'lb':90,
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
