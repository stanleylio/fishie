name = '(TBD)'
location = '"A booth in the Midwest"'
note = 'SeapHOx pH Sensor'
#latitude = 21.451592
#longitude = -157.796580

conf = [
    {
        'dbtag':'ts',
        'description':'(derived from date_code and time_code)',
        'interval':20*60,
    },
    {
        'dbtag':'idx',
        'unit':'-',
        'description':'-',
        'lb':0,
        'interval':20*60,
    },
    {
        'dbtag':'tC',
        'unit':'\u2103',
        'description':'CTD temperature',
        'lb':10,
        'ub':50,
        'interval':20*60,
    },
    {
        'dbtag':'epH',
        'description':'FET|EXT calculated pH in total scale',
        'lb':7,
        'ub':8.5,
        'interval':20*60,
    },
    {
        'dbtag':'ipH',
        'description':'FET|INT calculated pH in total scale',
        'lb':7,
        'ub':8.5,
        'interval':20*60,
    },
    {
        'dbtag':'pHC',
        'unit':'\u2103',
        'description':'ISFET Thermistor temperature',
        'lb':10,
        'ub':50,
        'interval':20*60,
    },
    {
        'dbtag':'dbar',
        'unit':'dbar',
        'description':'Pressure',
        'lb':0,
        'interval':20*60,
    },
    {
        'dbtag':'psu',
        'unit':'psu',
        'description':'CTD salinity',
        'lb':10,
        'ub':40,
        'interval':20*60,
    },
    {
        'dbtag':'ec_S_m',
        'unit':'S/m',
        'description':'Conductivity (CTD)',
        'lb':10,
        'ub':60,
        'interval':20*60,
    },
    {
        'dbtag':'o2_mg_L',
        'unit':'mg/L',
        'description':'Dissolved oxygen',
        'lb':0,
        'ub':10,
        'interval':20*60,
    },
    {
        'dbtag':'rh',
        'unit':'%',
        'description':'Electronics compartment relative humidity',
        'ub':70,
        'interval':20*60,
    },
    {
        'dbtag':'iC',
        'unit':'\u2103',
        'description':'Internal temperature',
        'interval':20*60,
    },
    {
        'dbtag':'sn',
        'description':'Serial Number',
        'interval':20*60,
    },

    {
        'dbtag':'Vb',
        'unit':'V',
        'description':'Relay dongle battery voltage',
        'lb':2.5,
        'ub':5.2,
        'interval':20*60,
    },
    {
        'dbtag':'Vs',
        'unit':'V',
        'description':'Solar panel voltage',
        'lb':0,
        'ub':7.5,
        'interval':20*60,
    },
]


if '__main__' == __name__:
    for c in conf:
        print('- - -')
        for k, v in c.items():
            print(k, ':', v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf, basename(__file__).split('.')[0].replace('_', '-'))
