name = 'Ala Wai Canal FDOM'
location = 'Hawaii Yacht Club'
note = 'Fluorescent dissolved organic matter (FDOM), chlorophyll and turbidity (cellular FDOM 1720)'
latitude = 21.286437
longitude = -157.842810
deployment_status = 'decommissioned'

#coreid = '3d0041001047373333353132'

conf = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE NOT NULL',
        'description':'Sensor clock (POSIX)',
        'plot':True,
        'interval':12*60,
    },
    {
        'dbtag':'C',
        'description':'Chlorophyll (EX/EM: 470/695nm)',
        'unit':'ug/L',
        'lb':0,
        'ub':0.0306*(4130 - 49),
        'plot_range':7*24,
        'interval':12*60,
    },
    {
        'dbtag':'N',
        'description':'Turbidity (700nm)',
        'unit':'NTU',
        'lb':0,
        'ub':0.0848*(4130 - 50),
        'plot_range':7*24,
        'interval':12*60,
    },
    {
        'dbtag':'F',
        'description':'FDOM (EX/EM: 370/460nm)',
        'unit':'ppb',
        'lb':0,
        'ub':0.0909*(4130 - 48),
        'plot_range':7*24,
        'interval':12*60,
    },
    {
        'dbtag':'ch695',
        'description':'Chlorophyll raw count (695nm)',
        'unit':'-',
        'lb':0,
        'ub':4130,
        'plot_range':7*24,
        'interval':12*60,
    },
    {
        'dbtag':'ch700',
        'description':'Turbidity raw count (700nm)',
        'unit':'-',
        'lb':0,
        'ub':4130,
        'plot_range':7*24,
        'interval':12*60,
    },
    {
        'dbtag':'ch460',
        'description':'FDOM raw count (EX/EM: 370/460nm)',
        'unit':'-',
        'lb':0,
        'ub':4130,
        'plot_range':7*24,
        'interval':12*60,
    },
    {
        'dbtag':'Vb',
        'unit':'V',
        'description':'Battery voltage (telemetry relay\'s)',
        'lb':3.7,
        'ub':5.5,
        'interval':12*60,
    },
    {
        'dbtag':'SoC',
        'unit':'%',
        'description':'State of Charge (telemetry relay\'s)',
        'lb':30,
        'ub':100,
        'interval':12*60,
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
