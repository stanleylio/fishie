name = 'CTD (under maintenance)'
location = 'First Makaha'
note = 'Seabird 16plus V2 CTD (white Delrin)'
latitude = 21.433912
longitude = -157.805338
deployment_status = 'decommissioned'


# ***field names not verified*** can't find the manual
conf = [
    {
        'dbtag':'ticker',
        'description':'Broadcast sequence number',
        'plot':False,
        'lb':0,
    },
    {
        'dbtag':'Vb',
        'description':'Relay dongle battery voltage',
        'lb':3.0,
        'ub':4.3,
        'interval':5*60,
    },
    {
        'dbtag':'Vs',
        'description':'Solar panel voltage (after rectifier)',
        'lb':0,
        'ub':7.5,
        'interval':5*60,
    },
    {
        'dbtag':'s',
        'unit':'psu',
        'description':'Salinity',
    },
    {
        'dbtag':'d',
        'unit':'dbar',
        'description':'Pressure',
    },
    {
        'dbtag':'t',
        'unit':'Deg.C',
        'description':'Temperature',
    },
    {
        'dbtag':'c',
        'unit':'S/m',
        'description':'Conductivity',
        'lb':0,
    },
    {
        'dbtag':'v0',
        'unit':'V',
        'description':'Turbidity (raw volt)',
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
        print('- - -')
        for k, v in c.items():
            print(k, ':', v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf, basename(__file__).split('.')[0].replace('_', '-'))
