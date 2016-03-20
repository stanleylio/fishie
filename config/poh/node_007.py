# -*- coding: utf-8 -*-
tag = 'node-007'
name = 'Met. Station'
location = 'Mākāhā 1'
note = 'Meteorological Station'

#arch = 'rpi'

log_dir = './log'
plot_dir = '../www'

plot_range = 24*14

#xbee_port = '/dev/ttyAMA0'
xbee_port = '/dev/ttyO1'
xbee_baud = 115200

wait = 597

multi_sample = 5

import sys
sys.path.append('..')
from config.config_support import Range

# TODO: use dictionary indexed by dbtag
conf = [
    {
        'dbtag':'Timestamp',
        'dbtype':'TIMESTAMP',
        'comtag':'ts',
        'unit':None,
        'description':'Time of sampling',
        'plot':False,
    },
    {
        'dbtag':'P_180',
        'dbtype':'INTEGER',
        'comtag':'P_180',
        'unit':'Pa',
        'description':'Barometric Pressure',
        'plot':True,
        'range':Range(80e3,110e3),
    },
    {
        'dbtag':'T_180',
        'dbtype':'REAL',
        'comtag':'T_180',
        'unit':'Deg.C',
        'description':'Casing Temperature',
        'plot':True,
        'range':Range(-20,80),
    },
    {
        'dbtag':'P_280',
        'dbtype':'REAL',
        'comtag':'P_280',
        'unit':'kPa',
        'description':'Barometric Pressure (BME280)',
        'plot':True,
        'range':Range(80,120),
    },
    {
        'dbtag':'T_280',
        'dbtype':'REAL',
        'comtag':'T_280',
        'unit':'Deg.C',
        'description':'Air Temperature (BME280)',
        'plot':True,
        'range':Range(-10,60),
    },
    {
        'dbtag':'RH_280',
        'dbtype':'REAL',
        'comtag':'RH_280',
        'unit':'%',
        'description':'% Relative Humidity (BME280)',
        'plot':True,
        'range':Range(0,100),
    },
    {
        'dbtag':'UV_Si1145',
        'dbtype':'REAL',
        'comtag':'UV_Si1145',
        'unit':'(100x index)',
        'description':'UV Index x 100',
        'plot':True,
    },
    {
        'dbtag':'IR_Si1145',
        'dbtype':'REAL',
        'comtag':'IR_Si1145',
        'unit':'lux',
        'description':'IR',
        'plot':True,
    },
    {
        'dbtag':'Amb_Si1145',
        'dbtype':'REAL',
        'comtag':'Amb_Si1145',
        'unit':'lux',
        'description':'Ambient Light Intensity',
        'plot':True,
    },
    {
        'dbtag':'Wind_average',
        'dbtype':'REAL',
        'comtag':'Wind_avg',
        'unit':'m/s',
        'description':'Wind Speed (average)',
        'plot':True,
        'range':Range(0,32.4),
    },
    {
        'dbtag':'Wind_gust',
        'dbtype':'REAL',
        'comtag':'Wind_gust',
        'unit':'m/s',
        'description':'Wind Speed (gust)',
        'plot':True,
        'range':Range(0,32.4),
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

