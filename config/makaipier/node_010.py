# -*- coding: utf-8 -*-
# us3
#tag = 'node-010'
name = 'Makai Pier Water Level'
location = 'Makai Research Pier'
note = 'Ultrasonic tide gauge'

plot_range = 24*7
data_source = 'mysql+mysqldb://{user}:{password}@localhost/uhcm'


#import sys
#sys.path.append('..')
from node.config.config_support import Range

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
        'range':Range(lb=2.5),  # lithium cell, shouldn't go above 4.2V
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v
