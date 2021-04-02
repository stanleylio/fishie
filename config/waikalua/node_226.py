name = 'pH, O2, conductivity'
location = '(TBD)'
note = 'SeaFET pH Sensor'
#latitude = 21.451592
#longitude = -157.796580
deployment_status = 'decommissioned'


conf = [
    {
        'dbtag':'ts',
        'description':'(derived from date_code and time_code)',
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
    {
        'dbtag':'date_code',
        'description':'Sample Date (UTC) in format, YYYYDDD',
        'plot':False,
        'interval':20*60,
    },
    {
        'dbtag':'time_code',
        'description':'Sample Time (UTC) in format, DESCIMALHOUR',
        'plot':False,
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
        'dbtag':'epH',
        'description':'FET|EXT calculated pH in total scale',
        'lb':7,
        'ub':8.5,
        'interval':20*60,
    },
    {
        'dbtag':'pHC',
        'unit':'Deg\u00b0C',
        'description':'ISFET Thermistor temperature',
        'lb':10,
        'ub':50,
        'interval':20*60,
    },
    {
        'dbtag':'tC',
        'unit':'Deg.C',
        'description':'CTD temperature',
        'lb':10,
        'ub':50,
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
        'dbtag':'o2_mg_L',
        'unit':'ml/L',
        'description':'CTD oxygen concentration',
        'lb':0,
        'ub':10,
        'interval':20*60,
    },
#    {
#        'dbtag':'P_CTD',
#        'unit':'dbar',
#        'description':'CTD pressure',
#        'plot':False,
#    },
    {
        'dbtag':'rh',
        'unit':'%',
        'description':'Electronics compartment relative humidity',
        'ub':70,
        'interval':20*60,
    },
    {
        'dbtag':'Vbm',
        'unit':'V',
        'description':'Main battery pack voltage',
        'interval':20*60,
    },
    {
        'dbtag':'Vbiso',
        'unit':'V',
        'description':'Isolated battery pack voltage',
        'interval':20*60,
    },
    {
        'dbtag':'sn',
        'description':'Serial Number',
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
