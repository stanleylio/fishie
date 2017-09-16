# -*- coding: utf-8 -*-
# kph2
name = 'Coco'
location = 'Site #4, Kāneʻohe Bay'
note = 'SeaFET pH Sensor; pole on a pole on a reef'

#interval = 15*60   # second
#plot_range = 24*7  # hour
#data_source = '/home/nuc/node/www/poh/storage/sensor_data.db'


conf = [
    {
        'dbtag':'ticker',
        'dbtype':'INTEGER',
        'description':'Voltage report sequence number',
        'lb':0,
        'interval':60*60,
    },
    {
        'dbtag':'Vbatt',
        'unit':'V',
        'description':'Relay dongle battery voltage',
        'lb':2.5,
        'ub':5.2,
        'interval':60*60,
    },
    {
        'dbtag':'DATE',
        'dbtype':'INTEGER',
        'description':'Sample Date (UTC) in format, YYYYDDD',
        'plot':False,
    },
    {
        'dbtag':'TIME',
        'description':'Sample Time (UTC) in format, DESCIMALHOUR',
        'plot':False,
    },
    {
        'dbtag':'PH_INT',
        'description':'FET|INT calculated pH in total scale',
        'lb':7,
        'ub':8.5,
    },
    {
        'dbtag':'PH_EXT',
        'description':'FET|EXT calculated pH in total scale',
        'lb':7,
        'ub':8.5,
    },
    {
        'dbtag':'TEMP',
        'unit':'Deg.C',
        'description':'ISFET Thermistor temperature',
    },
    {
        'dbtag':'TEMP_CTD',
        'unit':'Deg.C',
        'description':'CTD temperature',
    },
    {
        'dbtag':'S_CTD',
        'unit':'psu',
        'description':'CTD salinity',
    },
    {
        'dbtag':'O_CTD',
        'unit':'ml/L',
        'description':'CTD oxygen concentration',
    },
    {
        'dbtag':'P_CTD',
        'unit':'dbar',
        'description':'CTD pressure',
        'plot':False,
    },
    {
        'dbtag':'Vrs_FET_INT',
        'unit':'V',
        'description':'FET|INT voltage',
        'plot':False,
    },
    {
        'dbtag':'Vrs_FET_EXT',
        'unit':'V',
        'description':'FET|EXT voltage',
        'plot':False,
    },
    {
        'dbtag':'V_THERM',
        'unit':'V',
        'description':'Thermistor voltage',
        'plot':False,
    },
    {
        'dbtag':'V_SUPPLY',
        'unit':'V',
        'description':'Supply voltage',
        'plot':False,
    },
    {
        'dbtag':'I_SUPPLY',
        'unit':'mA',
        'description':'Supply current',
        'plot':False,
    },
    {
        'dbtag':'HUMIDITY',
        'unit':'%',
        'description':'Electronics compartment relative humidity',
    },
    {
        'dbtag':'V_5V',
        'unit':'V',
        'description':'Internal 5V supply voltage',
        'plot':False,
    },
    {
        'dbtag':'V_MBATT',
        'unit':'V',
        'description':'Main battery pack voltage',
    },
    {
        'dbtag':'V_ISO',
        'unit':'V',
        'description':'Internal isolated supply voltage',
        'plot':False,
    },
    {
        'dbtag':'V_ISOBATT',
        'unit':'V',
        'description':'Isolated battery pack voltage',
    },
    {
        'dbtag':'I_B',
        'unit':'nA',
        'description':'Substrate leakage current',
        'plot':False,
    },
    {
        'dbtag':'I_K',
        'unit':'nA',
        'description':'Counter electrode leakage current',
        'plot':False,
    },
    {
        'dbtag':'V_K',
        'unit':'V',
        'description':'Counter electrode voltage',
        'plot':False,
    },
    {
        'dbtag':'STATUS',
        'dbtype':'TEXT',
        'description':'Status word',
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
    
