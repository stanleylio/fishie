# -*- coding: utf-8 -*-
name = 'Cellular test bed'
location = 'UH Manoa'
note = 'Cellular ultrasonic tide gauge. Each sample is average of 60 measurements, made once a second. Transmission after every 10 samples are collected. Firmware p5d, hardware v0.2.'

coreid = '410055001951353338363036'


conf = [
    {
        'dbtag':'Timestamp',
        'description':'Sample time (Electron clock)',
    },
    {
        'dbtag':'d2w',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'lb':300,
        'ub':5000,
    },
    {
        'dbtag':'p',
        'unit':'hPa',
        'description':'Barometric pressure (BME280)',
        'lb':800,
        'ub':1200,
    },
    {
        'dbtag':'t',
        'unit':'Deg.C',
        'description':'Air temperature (BME280)',
        'lb':-10,
        'ub':60,
    },
    {
        'dbtag':'rh',
        'unit':'%',
        'description':'% Relative humidity (BME280)',
        'lb':0,
        'ub':100,
    },
    {
        'dbtag':'VbattV',
        'unit':'V',
        'description':'Battery voltage',
        'lb':3.7,
        'ub':5.5,
    },
    {
        'dbtag':'SoC',
        'unit':'%',
        'description':'State of Charge',
        'lb':0,
        'ub':100,
    },
    {
        'dbtag':'sample_size',
        'description':'Number of valid readings in the 60 measurements',
        'lb':0,
        'ub':60,
    },
]


if '__main__' == __name__:
    for c in conf:
        print('- - -')
        for k,v in c.iteritems():
            print(k,':',v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf,basename(__file__).split('.')[0].replace('_','-'))
