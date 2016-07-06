# -*- coding: utf-8 -*-
# water tank
tag = 'node-026'
name = 'Hollie\'s'
location = 'under the shade'
note = 'Apex sensors in several water tanks, sampled at one sample/minute via public XML feed (not RSS)'
# perhaps I should put the dbfile here and remove the magical get_dbfile() function. TODO
#dbfile = '/home/nuc/data/htank/storage/sensor_data.db'

plot_range = 24*7

#import sys
#sys.path.append('..')
from config.config_support import Range

conf = [
    {
        'dbtag':'ReceptionTime',
        'dbtype':'TIMESTAMP',
        'comtag':None,
        'unit':None,
        'description':'Server time',
        'plot':False,
    },
    {
        'dbtag':'apex_time',
        'dbtype':'TEXT',
        'comtag':None,
        'unit':None,
        'description':'Sensor\'s reported time',
        'plot':False,
    },
    {
        'dbtag':'pH_13',
        'dbtype':'REAL',
        'comtag':None,
        'unit':None,
        'description':'pH.13',
        'plot':True,
        'range':Range(6,10),
    },
    {
        'dbtag':'pH_14',
        'dbtype':'REAL',
        'comtag':None,
        'unit':None,
        'description':'pH.14',
        'plot':True,
        'range':Range(6,10),
    },
    {
        'dbtag':'pH_15',
        'dbtype':'REAL',
        'comtag':None,
        'unit':None,
        'description':'pH.15',
        'plot':True,
        'range':Range(6,10),
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

