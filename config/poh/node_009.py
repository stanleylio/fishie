# -*- coding: utf-8 -*-
# us2
tag = 'node-009'
name = 'Mākāhā 1 Water Depth'
location = 'Mākāhā 1'
note = 'Ultrasonic Proof of Concept'

log_dir = './log'
plot_dir ='../www'

plot_range = 24*7

#wait = 400
#multi_sample = 7

import sys
sys.path.append('..')
from config.config_support import Range

# TODO: use dictionary indexed by dbtag
conf = [
    {
        'dbtag':'ticker',
        'dbtype':'INTEGER',
        'comtag':None,
        'unit':None,
        'description':'Ticker',
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
        'dbtag':'VbattmV',
        'dbtype':'INTEGER',
        'comtag':None,
        'unit':'mV',
        'description':'Battery voltage (Vcc)',
        'plot':True,
        'range':Range(0,4500),  # lithium cell, shouldn't go above 4.2V
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

