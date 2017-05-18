# -*- coding: utf-8 -*-
# us5
#tag = 'node-012'
name = 'Ultrasonic tide gauge'
location = 'Nowhere. Not deployed.'
note = 'Ultrasonic tide gauge (us5). One-minute interval. Not deployed'

#plot_range = 24*7
data_source = 'mysql+mysqldb://{user}:{password}@localhost/uhcm'


#import sys
#sys.path.append('..')
#from node.config.config_support import Range

conf = [
    {
        'dbtag':'Timestamp',
        'dbtype':'REAL',
        'comtag':'ts',
        'description':'Sampling time (by base station)',
        'plot':False,
    },
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
        'description':'Distance from rim of sensor to water surface',
        'lb':300,
        'ub':5000,
    },
    {
        'dbtag':'VbattV',
        'dbtype':'REAL',
        'unit':'V',
        'description':'Battery voltage (Vcc)',
        'lb':2.5,
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
    
