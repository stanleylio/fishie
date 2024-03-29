name = 'Dissolved Oxygen (Hīhīmanu)'
location = ''
note = 'Aanderaa oxygen optode 4531. Hardware v5.4.'
latitude = 21.433912
longitude = -157.805338
deployment_status = 'decommissioned'

conf = [
    {
        'dbtag':'sn',
        'unit':'-',
        'description':'Sensor serial number',
        'interval':5*60,
    },
    {
        'dbtag':'O2',
        'unit':'uM',
        'description':'Dissolved oxygen',
        'lb':100,
        'ub':300,
        'interval':5*60,
    },
    {
        'dbtag':'air',
        'unit':'%',
        'description':'Air saturation',
        'lb':50,
        'interval':5*60,
    },
    {
        'dbtag':'Tw',
        'unit':'\u2103',
        'description':'Water temperature',
        'lb':-5,
        'ub':40,
        'interval':5*60,
    },
    {
        'dbtag':'Vb',
        'description':'Battery voltage',
        'unit':'V',
        'lb':3.0,
        'ub':4.3,
        'interval':5*60,
    },
    {
        'dbtag':'Vs',
        'description':'Solar panel voltage (after rectifier)',
        'unit':'V',
        'lb':0,
        'ub':7.5,
        'interval':5*60,
    },
    {
        'dbtag':'idx',
        'description':'Sample index',
        'lb':24*60*60/(5*60),
        'interval':5*60,
    },
    {
        'dbtag':'c',
        'description':'1Hz ticker',
        'lb':24*60*60,
        'interval':5*60,
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
