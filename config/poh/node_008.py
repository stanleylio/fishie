# -*- coding: utf-8 -*-
name = 'Water Level (Kahoʻokele)'
location = 'Kahoʻokele (second mākāhā)'
note = 'XBee ultrasonic tide gauge. One sample per minute. Each sample is the sample mean of the past 60 measurements taken at 1Hz. Telemetry only. No RTC. 7\'4" to bottom. Deployed May 22, 2017. Hardware v5.0, firmware us11c.'
latitude = 21.435435
longitude = -157.805250

# 20170522
#UPDATE uhcm.`node-008` SET VbattmV=VbattmV/1000.0;

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
        'dbtag':'Vs',
        'unit':'V',
        'description':'Solar input voltage',
        'lb':0,
        'ub':6.0,
        'interval':60,
    },
    {
        'dbtag':'idx',
        'description':'Sample index',
        'lb':0,
        'interval':60,
    },
    {
        'dbtag':'sc',
        'description':'Sample Size (after rejecting invalid measurements)',
        'lb':0,
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
