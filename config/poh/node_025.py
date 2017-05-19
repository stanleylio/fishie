# -*- coding: utf-8 -*-
# seabird1
#tag = 'node-025'
name = 'Seabird CTD #1'
location = 'First Makaha'
note = 'Seabird CTD #1 (white Delrin)'

#plot_range = 24*7
#data_source = '/home/nuc/node/www/poh/storage/sensor_data.db'

# ***field names not verified*** can't find the manual
conf = [
    {
        'dbtag':'ticker',
        'description':'Broadcast sequence number',
        'plot':False,
        'lb':0,
    },
    {
        'dbtag':'Vbatt',
        'unit':'V',
        'description':'Relay dongle battery voltage',
        'lb':2.5,
    },
    {
        'dbtag':'salinity_seabird',
        'unit':'psu',
        'description':'Salinity',
    },
    {
        'dbtag':'pressure_seabird',
        'unit':'dbar',
        'description':'Pressure',
    },
    {
        'dbtag':'temperature_seabird',
        'unit':'Deg.C',
        'description':'Temperature',
    },
    {
        'dbtag':'conductivity_seabird',
        'unit':'S/m',
        'description':'Conductivity',
        'lb':0,
    },
    {
        'dbtag':'v0_seabird',
        'description':'Turbidity (unconverted volt)',
    },
    {
        'dbtag':'dt_seabird',
        'dbtype':'TEXT',
        'description':'Seabird sensor time',
        'plot':False,
    },
    {
        'dbtag':'sn_seabird',
        'dbtype':'TEXT',
        'description':'Serial number',
        'plot':False,
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
    
