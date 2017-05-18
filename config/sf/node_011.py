# -*- coding: utf-8 -*-
# us4
#tag = 'node-011'
name = 'Ultrasonic tide gauge'
location = 'Foster City Lagoon, San Francisco, California'
note = 'Ultrasonic tide gauge (us4). One-minute interval, no solar charging.'

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
        'description':'Distance from base of sensor to water surface',
        'lb':300,
        'ub':5000,
    },
    {
        'dbtag':'VbattV',
        'dbtype':'REAL',
        'unit':'V',
        'description':'Battery voltage',
        'plot':True,
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
    
