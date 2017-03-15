# -*- coding: utf-8 -*-
# us1
name = 'Kahoʻokele (Mākāhā 2) Water Level'
location = 'Kahoʻokele (Mākāhā 2)'
note = 'Ultrasonic tide gauge (us1)'

log_dir = './log'
plot_dir ='../www'

data_source = '/home/nuc/node/www/poh/storage/sensor_data.db'

conf = [
    {
        'dbtag':'ticker',
        'dbtype':'INTEGER',
        'comtag':None,
        'unit':None,
        'description':'Broadcast sequence number',
        'plot':False,
        'lb':0,
    },
    {
        'dbtag':'d2w',
        'dbtype':'REAL',
        'comtag':None,
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'plot':True,
        'lb':300,
        'ub':5000,
    },
    {
        'dbtag':'VbattmV',
        'dbtype':'INTEGER',
        'comtag':None,
        'unit':'mV',
        'description':'Battery voltage (Vcc)',
        'plot':True,
        'lb':2400,
        'ub':4250,
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
    conf.insert(0,{'dbtag':'ReceptionTime','dbtype':'DOUBLE NOT NULL'})
    create_table(conf,__file__.split('.')[0].replace('_','-'))
    
