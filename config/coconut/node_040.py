name = '"Water-Under-The-Bridge"'
location = 'Coconut Island'
google_earth_link = 'https://goo.gl/maps/8gJTDCgVan32'
note = 'Ultrasonic tide gauge measuring distance to water surface from fixed structure. One measurement per second, one transmission (average of past minute) per minute. Hardware v4.2, firmware us10b.'
latitude = 21.435983
longitude = -157.788333
deployment_status = 'decommissioned'


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
        'dbtag':'VbattV',
        'unit':'V',
        'description':'Battery voltage (Vbatt)',
        'lb':2.7,
        'interval':60,
    },
    {
        'dbtag':'ticker',
        'description':'1Hz ticker',
        'lb':0,
        'interval':60,
    },
    {
        'dbtag':'sample_size',
        'description':'Number of valid readings in the 60 measurements',
        'lb':0,
        'ub':60,
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
