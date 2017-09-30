# -*- coding: utf-8 -*-
# us2
name = 'Hīhīmanu Water Level'
location = 'Hīhīmanu (first mākāhā)'
note = 'Ultrasonic tide gauge (us2)'

#log_dir = './log'
#plot_dir ='../www'

#data_source = '/home/nuc/node/www/poh/storage/sensor_data.db'

conf = [
    {
        'dbtag':'ticker',
        'dbtype':'INTEGER',
        'description':'Broadcast sequence number',
        'plot':False,
        'lb':0,
    },
    {
        'dbtag':'d2w',
        'dbtype':'REAL',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'lb':300,
        'ub':5000,
    },
    {
        'dbtag':'VbattmV',
        'dbtype':'INTEGER',
        'unit':'mV',
        'description':'Battery voltage (Vcc)',
        'lb':2400,
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
    
