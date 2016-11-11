# -*- coding: utf-8 -*-
# us3
tag = 'node-010'
name = 'River Mākāhā Water Level'
location = 'River Mākāhā'
note = 'Ultrasonic tide gauge'

log_dir = './log'
plot_dir ='../www'

plot_range = 24*7

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
        'description':'Distance from rim of sensor to water surface',
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
        'range':Range(lb=2.5),  # lithium cell, shouldn't go above 4.2V
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

