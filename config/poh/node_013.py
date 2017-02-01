# -*- coding: utf-8 -*-
name = 'Water Depth'
location = 'River Mākāhā'
note = 'Ultrasonic tide gauge'

INTERVAL = 60
NGROUP = 11

#LOGDIR = '/var/uhcm/log'
#DBPATH = '/var/uhcm/storage/sensor_data.db'


from node.config.config_support import Range


conf = [
    {
        'dbtag':'ts',
        'dbtype':'REAL',
        'comtag':'ts',
        'unit':None,
        'description':'Reception time (at base station)',
        'plot':False,
    },
    {
        'dbtag':'d2w',
        'dbtype':'REAL',
        'comtag':'d2w',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'plot':True,
        'range':Range(300,5000),
    },
    {
        'dbtag':'VbattV',
        'dbtype':'REAL',
        'comtag':'VbattV',
        'unit':'V',
        'description':'Battery voltage (Vbatt)',
        'plot':True,
        'range':Range(lb=2400),
    },
    {
        'dbtag':'ticker',
        'dbtype':'REAL',
        'comtag':'ticker',
        'unit':None,
        'description':'1Hz ticker',
        'plot':True,
        'range':Range(lb=0),
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

