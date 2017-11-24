# -*- coding: utf-8 -*-
name = 'MSB Meteological Station'
location = 'Marine Science Building Rooftop'
note = 'RM Young 05106 Anemometer'


INTERVAL = 60
NGROUP = 7


conf = [
    {
        'dbtag':'Timestamp',
        'dbtype':'DOUBLE NOT NULL',
        'description':'Time of sampling',
        'plot':False,
        'interval':1,
    },
    {
        'dbtag':'wind_mps',
        'description':'Wind speed',
        'unit':'m/s',
        'lb':0,
        'plot_range':2*24,
        'interval':1,
    },
    {
        'dbtag':'wind_dir_deg',
        'description':'Wind direction',
        'unit':'Deg',
        'lb':0,
        'ub':360,
        'plot_range':2*24,
        'interval':1,
    },
    {
        'dbtag':'P_int',
        'unit':'kPa',
        'description':'Barometric pressure (BME280)',
        'lb':80,
        'ub':120,
        'plot_range':7*24,
        'interval':60,
    },
    {
        'dbtag':'T_int',
        'unit':'Deg.C',
        'description':'Housing temperature (BME280)',
        'lb':-10,
        'ub':60,
        'plot_range':7*24,
        'interval':60,
    },
    {
        'dbtag':'RH_int',
        'unit':'%',
        'description':'Housing % Relative humidity (BME280)',
        'lb':0,
        'ub':100,
        'plot_range':7*24,
        'interval':60,
    },
    {
        'dbtag':'P_ext',
        'unit':'kPa',
        'description':'Barometric pressure (BME280)',
        'lb':80,
        'ub':120,
        'plot_range':7*24,
        'interval':60,
    },
    {
        'dbtag':'T_ext',
        'unit':'Deg.C',
        'description':'Air temperature (BME280)',
        'lb':-10,
        'ub':60,
        'plot_range':7*24,
        'interval':60,
    },
    {
        'dbtag':'RH_ext',
        'unit':'%',
        'description':'% Relative humidity (BME280)',
        'lb':0,
        'ub':100,
        'plot_range':7*24,
        'interval':60,
    },
    {
        'dbtag':'system_clock',
        'description':'Device clock',
        'interval':60,
    },
    {
        'dbtag':'uptime_second',
        'description':'Uptime in seconds',
        'interval':60,
    },
    {
        'dbtag':'usedMB',
        'unit':'MB',
        'description':'Used disk space',
        'interval':60,
    },
    {
        'dbtag':'freeMB',
        'unit':'MB',
        'description':'Free disk space',
        'lb':10000,
        'interval':60,
    },
    {
        'dbtag':'VbattV',
        'unit':'V',
        'description':'12V SLA battery voltage',
        'lb':12,
        'ub':14,
        'interval':60,
    },
]


if '__main__' == __name__:
    for c in conf:
        print('- - -')
        for k,v in c.iteritems():
            print(k,':',v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf,basename(__file__).split('.')[0].replace('_','-'))
