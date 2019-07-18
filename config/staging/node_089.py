# -*- coding: utf-8 -*-
name = '"Zuko"'
location = '(TBD)'
google_earth_link = '#'
note = 'Ultrasonic tide gauge (XBee). 1Hz measurements. Each transmission is average of 60 measurements. Firmware us13b, hardware v5.3.'


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
        'lb':0,
        'interval':60,
    },
    {
        'dbtag':'c',
        'description':'Internal 1Hz counter',
        'lb':24*60*60,
        'interval':60,
    },
]

'''
    {
        'dbtag':'t',
        'unit':'Deg.C',
        'description':'Housing temperature (BME280)',
        'lb':10,
        'ub':50,
        'interval':60,
    },
    {
        'dbtag':'p',
        'unit':'kPa',
        'description':'Housing (barometric) pressure (BME280)',
        'lb':80,
        'ub':120,
        'interval':60,
    },
    {
        'dbtag':'rh',
        'unit':'%',
        'description':'Housing % relative humidity (BME280)',
        'lb':10,
        'ub':80,
        'interval':60,
    },
'''


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
