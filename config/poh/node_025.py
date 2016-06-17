# -*- coding: utf-8 -*-
# seabird1
tag = 'node-025'
name = 'Seabird CTD #1 (white Delrin)'
location = 'middle of the pond'
note = 'Sea-bird CTD #1'

plot_range = 24*7

#import sys
#sys.path.append('..')
from config.config_support import Range

# TODO: use dictionary indexed by dbtag
# ***field names not verified*** can't find the manual
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
        'dbtag':'Vbatt',
        'dbtype':'REAL',
        'comtag':None,
        'unit':'V',
        'description':'Battery voltage',
        'plot':True,
        #'range':Range(2.5,4.2),  # lithium cell, shouldn't go above 4.2V
        'range':Range(lb=2.5),
    },
    {
        'dbtag':'salinity_seabird',
        'dbtype':'REAL',
        'comtag':'sal',
        'unit':None,
        'description':'Salinity (Seabird CTD)',
        'plot':True,
        #'range':Range(2.5,4.2),
    },
    {
        'dbtag':'pressure_seabird',
        'dbtype':'REAL',
        'comtag':'p1',
        'unit':None,
        'description':'Pressure (Seabird CTD)',
        'plot':True,
    },
    {
        'dbtag':'temperature_seabird',
        'dbtype':'REAL',
        'comtag':'t1',
        'unit':'Deg.C',
        'description':'Temperature (Seabird CTD)',
        'plot':True,
    },
    {
        'dbtag':'conductivity_seabird',
        'dbtype':'REAL',
        'comtag':'c1',
        'unit':None,
        'description':'Conductivity (Seabird CTD)',
        'plot':True,
        'range':Range(lb=0),
    },
    {
        'dbtag':'v0_seabird',
        'dbtype':'REAL',
        'comtag':'v0',
        'unit':None,
        'description':'no idea what this is (Seabird CTD)',
        'plot':True,
    },
    {
        'dbtag':'dt_seabird',
        'dbtype':'TIMESTAMP',
        'comtag':'dt',
        'unit':None,
        'description':'Seabird time (Seabird CTD)',
        'plot':False,
    },
    {
        'dbtag':'sn_seabird',
        'dbtype':'TEXT',
        'comtag':'sn',
        'unit':None,
        'description':'Serial number (Seabird CTD)',
        'plot':False,
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

