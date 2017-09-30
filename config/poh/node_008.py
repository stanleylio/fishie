# -*- coding: utf-8 -*-
name = 'Kahoʻokele Water Level'
location = 'Kahoʻokele (second mākāhā)'
note = 'Ultrasonic tide gauge (v4.1). One sample per minute; each sample is the sample mean of the past 60 measurements taken at 1Hz. Telemetry only. No RTC; 7\'4" to bottom. Deployed May 22, 2017'

#log_dir = './log'
#plot_dir ='../www'

#data_source = '/home/nuc/node/www/poh/storage/sensor_data.db'

# 20170522
#UPDATE uhcm.`node-008` SET VbattmV=VbattmV/1000.0;

conf = [
    {
        'dbtag':'d2w',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'lb':300,
        'ub':5000,
    },
    {
        'dbtag':'VbattV',
        'unit':'V',
        'description':'Battery voltage (Vbatt)',
        'lb':2.4,
    },
    {
        'dbtag':'ticker',
        'description':'1Hz ticker',
        'lb':0,
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

    import sys
    sys.path.append('../..')
    from storage.storage2 import create_table
    create_table(conf,__file__.split('.')[0].replace('_','-'))
    
