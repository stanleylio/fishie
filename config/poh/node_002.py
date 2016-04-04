# -*- coding: utf-8 -*-
tag = 'node-002'
name = 'Fish pan'
location = 'Mākāhā 1'
note = 'Aanderaa 4330f + MS5803-14BA + EZO EC + BMP180'

log_dir = './log'
plot_dir = '../www'

plot_range = 24*7

xbee_port = '/dev/ttyO1'
xbee_baud = 115200

optode_port = '/dev/ttyO2'

wait = 592
#wait = 0

multi_sample = 7

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
        #'convf':lambda (x): x/1e3,
        #'convunit':'kPa',
    },
    {
        'dbtag':'T_180',
        'dbtype':'REAL',
        'comtag':'T_180',
        'unit':'Deg.C',
        'description':'Casing Temperature',
        'plot':True,
        'range':Range(-10,80),
    },
    {
        'dbtag':'P_5803',
        'dbtype':'REAL',
        'comtag':'P_5803',
        'unit':'kPa',
        'description':'Water Pressure',
        'plot':True,
        'range':Range(80,150),
    },
    {
        'dbtag':'T_5803',
        'dbtype':'REAL',
        'comtag':'T_5803',
        'unit':'Deg.C',
        'description':'Water Temperature (5803)',
        'plot':True,
        'range':Range(-10,60),
    },
    {
        'dbtag':'ec',
        'dbtype':'REAL',
        'comtag':'ec',
        'unit':'uS/cm',
        'description':'Conductivity',
        'plot':True,
        'range':Range(0,55e3),
    },
    {
        'dbtag':'sal',
        'dbtype':'REAL',
        'comtag':'sal',
        'unit':'(ppt)',
        'description':'Salinity',
        'plot':False,
        'range':Range(lb=0),
    },
    {
        'dbtag':'O2Concentration',
        'dbtype':'REAL',
        'comtag':'O2',
        'unit':'uM',
        'description':'Oxygen Concentration',
        'plot':True,
        'range':Range(0,450),
    },
    {
        'dbtag':'AirSaturation',
        'dbtype':'REAL',
        'comtag':'Air',
        'unit':'%',
        'description':'Air Saturation',
        'plot':True,
        'range':Range(0,150),
    },
    {
        'dbtag':'Temperature',
        'dbtype':'REAL',
        'comtag':'T_4330f',
        'unit':'Deg.C',
        'description':'Water Temperature (4330F)',
        'plot':True,
        'range':Range(-10,60),
    },
    {
        'dbtag':'CalPhase',
        'dbtype':'REAL',
        'comtag':'CalPhase',
        'unit':'Deg',
        'description':'CalPhase',
        'plot':False,
    },
    {
        'dbtag':'TCPhase',
        'dbtype':'REAL',
        'comtag':'TCPhase',
        'unit':'Deg',
        'description':'TCPhase',
        'plot':False,
    },
    {
        'dbtag':'C1RPh',
        'dbtype':'REAL',
        'comtag':'C1RPh',
        'unit':'Deg',
        'description':'C1RPh',
        'plot':False,
    },
    {
        'dbtag':'C2RPh',
        'dbtype':'REAL',
        'comtag':'C2RPh',
        'unit':'Deg',
        'description':'C2RPh',
        'plot':False,
    },
    {
        'dbtag':'C1Amp',
        'dbtype':'REAL',
        'comtag':'C1Amp',
        'unit':'mV',
        'description':'C1Amp',
        'plot':False,
    },
    {
        'dbtag':'C2Amp',
        'dbtype':'REAL',
        'comtag':'C2Amp',
        'unit':'mV',
        'description':'C2Amp',
        'plot':False,
    },
    {
        'dbtag':'RawTemp',
        'dbtype':'REAL',
        'comtag':'RawTemp',
        'unit':'mV',
        'description':'RawTemp',
        'plot':False,
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

