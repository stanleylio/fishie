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
from node.config.config_support import Range

conf = [
    {
        'dbtag':'Timestamp',
        'dbtype':'REAL',
        'comtag':'ts',
        'unit':None,
        'description':'Sampling time (by base station)',
        'plot':False,
    },
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
        'dbtag':'VbattV',
        'dbtype':'REAL',
        'comtag':None,
        'unit':'V',
        'description':'Battery voltage (Vcc)',
        'plot':True,
        #'range':Range(0,4500),  # lithium cell, shouldn't go above 4.2V
        'range':Range(lb=2400),
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

