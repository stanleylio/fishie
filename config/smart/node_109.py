# -*- coding: utf-8 -*-
name = 'Makiki Weather Station'
location = 'Halau Ku Mana School (21.313060, -157.829150)'
note = 'Rain, air temperature, barometric pressure, and humidity. Solar, Arduino + XBee'


conf = [
    {
        'dbtag':'ts',
        'description':'Time of sampling',
        'plot':True,
        'interval':60,
    },
    {
        'dbtag':'p',
        'unit':'kPa',
        'description':'Barometric pressure (BME280)',
        'lb':80,
        'ub':120,
        'plot_range':7*24,
        'interval':60,
    },
    {
        'dbtag':'t',
        'unit':'Deg.C',
        'description':'Temperature (BME280)',
        'lb':-10,
        'ub':60,
        'plot_range':7*24,
        'interval':60,
    },
    {
        'dbtag':'rh',
        'unit':'%',
        'description':'% Relative humidity (BME280)',
        'lb':0,
        'ub':100,
        'plot_range':7*24,
        'interval':60,
    },
    {
        'dbtag':'rain_bucket_tipped',
        'unit':'-',
        'description':'-',
        'lb':1,
        'plot_range':7*24,
        'interval':365*24*60*60,
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
