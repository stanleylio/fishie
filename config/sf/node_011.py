# -*- coding: utf-8 -*-
# us4
tag = 'node-011'
name = '-'
location = '-'
note = 'Ultrasonic tide gauge (us4)'

plot_range = 24*7
data_source = '/home/nuc/node/www/sf/storage/sensor_data.db'


import sys
sys.path.append('..')
from config.config_support import Range

conf = [
    {
        'dbtag':'ticker',
        'dbtype':'INTEGER',
        'comtag':None,
        'unit':None,
        'description':'Broadcast sequence number',
        'plot':False,
        'range':Range(lb=0),
    },
    {
        'dbtag':'d2w',
        'dbtype':'REAL',
        'comtag':None,
        'unit':'mm',
        'description':'Distance from base of sensor to water surface',
        'plot':True,
        'range':Range(300,5000),
    },
    {
        'dbtag':'Vbatt',
        'dbtype':'REAL',
        'comtag':None,
        'unit':'V',
        'description':'Battery voltage',
        'plot':True,
        'range':Range(lb=2.5),
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

