# -*- coding: utf-8 -*-
tag = 'node-004'
name = 'First CTD'
location = 'Mākāhā 1'
note = 'CTD with Atlas Scientific sensor'

log_dir = './log'
plot_dir = '../www'

plot_range = 24*7

xbee_port = '/dev/ttyO1'
xbee_baud = 115200

# consider how node-specific these are... should really put them in
# sampling.py instead.

optode_port = '/dev/ttyO2'

wait = 594

import sys
sys.path.append('..')
from config.config_support import Range

# I'm starting to regret the decision of putting the config in separate files.
# dynamic importing is a mess.

# TODO: use dictionary indexed by dbtag
conf = [
#    {
#        'dbtag':'How it is referenced in sampling.py and in the drivers',
#        'dbtype':'SQLite data type',
#        'comtag':'How it is identified in broadcast messages',
#        'unit':'physical unit of the readings',
#        'description':'as name',
#    },
    {
        'dbtag':'Timestamp',
        'dbtype':'TIMESTAMP',
        'comtag':'ts',
        'unit':None,
        'description':'Time of sampling',
        'plot':False,
    },
    {
        'dbtag':'ec',
        'dbtype':'REAL',
        'comtag':'ec',
        'unit':'uS/cm',
        'description':'Conductivity (EZO EC)',
        'plot':False,
        'range':Range(0,55e3),
    },
    {
        'dbtag':'sal',
        'dbtype':'REAL',
        'comtag':'sal',
        'unit':'(ppt)',
        'description':'Salinity (EZO EC)',
        'plot':False,
        'range':Range(lb=0),
    },
    {
        'dbtag':'P_180',
        'dbtype':'REAL',
        'comtag':'P_180',
        'unit':'Pa',
        'description':'Barometric pressure (BMP180)',
        'plot':True,
        'range':Range(90e3,110e3),
    },
    {
        'dbtag':'T_180',
        'dbtype':'REAL',
        'comtag':'T_180',
        'unit':'Deg.C',
        'description':'Enclosure temperature (BMP180)',
        'plot':True,
        'range':Range(-10,80),
    },
    {
        'dbtag':'P_5803',
        'dbtype':'REAL',
        'comtag':'P_5803',
        'unit':'kPa',
        'description':'Water pressure (MS5803-14BA)',
        'plot':True,
        'range':Range(80,150),
    },
    {
        'dbtag':'T_5803',
        'dbtype':'REAL',
        'comtag':'T_5803',
        'unit':'Deg.C',
        'description':'Water temperature (MS5803-14BA)',
        'plot':True,
        'range':Range(-10,60),
    },
    {
        'dbtag':'O2Concentration',
        'dbtype':'REAL',
        'comtag':'O2',
        'unit':'uM',
        'description':'Oxygen concentration (4330F)',
        'plot':True,
        'range':Range(0,450),
    },
    {
        'dbtag':'AirSaturation',
        'dbtype':'REAL',
        'comtag':'Air',
        'unit':'%',
        'description':'Air saturation (4330F)',
        'plot':True,
        'range':Range(0,150),
    },
    {
        'dbtag':'Temperature',
        'dbtype':'REAL',
        'comtag':'T_4330f',
        'unit':'Deg.C',
        'description':'Water temperature (4330F)',
        'plot':True,
        'range':Range(-20,60),
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

