# -*- coding: utf-8 -*-
name = 'Hīhīmanu Met. Station'
location = 'Hīhīmanu (first mākāhā)'
note = 'Meteorological Station'

log_dir = './log'
plot_dir = '../www'

#xbee_port = '/dev/ttyAMA0'
xbee_port = '/dev/ttyO1'
xbee_baud = 115200

wait = 597
multi_sample = 5


conf = [
    {
        'dbtag':'Timestamp',
        'dbtype':'DOUBLE NOT NULL',
        'description':'Time of sampling',
        'plot':False,
    },
    {
        'dbtag':'P_180',
        'dbtype':'INTEGER',
        'unit':'Pa',
        'description':'Barometric pressure (BMP180)',
        'lb':80e3,
        'ub':110e3,
    },
    {
        'dbtag':'T_180',
        'unit':'Deg.C',
        'description':'Enclosure temperature (BMP180)',
        'lb':-20,
        'ub':80,
    },
    {
        'dbtag':'P_280',
        'unit':'kPa',
        'description':'Barometric pressure (BME280)',
        'lb':80,
        'ub':120,
    },
    {
        'dbtag':'T_280',
        'unit':'Deg.C',
        'description':'Air temperature (BME280)',
        'lb':-10,
        'ub':60,
    },
    {
        'dbtag':'RH_280',
        'unit':'%',
        'description':'% Relative humidity (BME280)',
        'lb':0,
        'ub':100,
    },
    {
        'dbtag':'UV_Si1145',
        'unit':'(100x index)',
        'description':'UV Index x 100',
    },
    {
        'dbtag':'IR_Si1145',
        'unit':'lux',
        'description':'IR',
    },
    {
        'dbtag':'Amb_Si1145',
        'unit':'lux',
        'description':'Ambient light intensity',
    },
    {
        'dbtag':'Wind_avg',
        'unit':'m/s',
        'description':'Average wind speed',
        'lb':0,
        'ub':32.4,
    },
    {
        'dbtag':'Wind_gust',
        'unit':'m/s',
        'description':'Wind gust',
        'lb':0,
        'ub':32.4,
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

    import sys
    sys.path.append('../..')
    from storage.storage2 import create_table
    create_table(conf,__file__.split('.')[0].replace('_','-'))
    
