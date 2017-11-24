# -*- coding: utf-8 -*-
name = 'MSB Meteological Station'
location = 'Marine Science Building Rooftop'
note = 'RM Young 05106 Anemometer'


INTERVAL = 0.5


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
        'plot_range':2*24,
        'lb':0,
        'interval':1,
    },
    {
        'dbtag':'wind_dir_deg',
        'description':'Wind direction',
        'unit':'Deg',
        'plot_range':2*24,
        'lb':0,
        'ub':360,
        'interval':1,
    },
    {
        'dbtag':'P_int',
        'unit':'kPa',
        'description':'Barometric pressure (BME280)',
        'lb':80,
        'ub':120,
        'interval':1,
        'plot_range':2*24,
    },
    {
        'dbtag':'T_int',
        'unit':'Deg.C',
        'description':'Housing temperature (BME280)',
        'lb':-10,
        'ub':60,
        'interval':1,
        'plot_range':2*24,
    },
    {
        'dbtag':'RH_int',
        'unit':'%',
        'description':'Housing % Relative humidity (BME280)',
        'lb':0,
        'ub':100,
        'interval':1,
        'plot_range':2*24,
    },
    {
        'dbtag':'P_ext',
        'unit':'kPa',
        'description':'Barometric pressure (BME280)',
        'lb':80,
        'ub':120,
        'interval':1,
        'plot_range':2*24,
    },
    {
        'dbtag':'T_ext',
        'unit':'Deg.C',
        'description':'Air temperature (BME280)',
        'lb':-10,
        'ub':60,
        'interval':1,
        'plot_range':2*24,
    },
    {
        'dbtag':'RH_ext',
        'unit':'%',
        'description':'% Relative humidity (BME280)',
        'lb':0,
        'ub':100,
        'interval':1,
        'plot_range':2*24,
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
