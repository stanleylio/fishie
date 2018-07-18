# -*- coding: utf-8 -*-
name = '(TBD)'
location = '(TBD)'
note = '(TBD)'


INTERVAL = 60


conf = [
    {
        'dbtag':'Timestamp',
        'description':'Time of sampling (device clock)',
        'plot':True,
        'interval':INTERVAL,
    },
    {
        'dbtag':'p',
        'unit':'kPa',
        'description':'Barometric pressure (BME280)',
        'lb':90,
        'ub':110,
        'interval':INTERVAL,
    },
    {
        'dbtag':'t',
        'unit':'Deg.C',
        'description':'Enclosure temperature (BME280)',
        'lb':-10,
        'ub':70,
        'interval':INTERVAL,
    },
    {
        'dbtag':'rh',
        'unit':'%',
        'description':'Enclosure humidity (BME280)',
        'lb':20,
        'ub':90,
        'interval':INTERVAL,
    },
    {
        'dbtag':'v',
        'description':'Wind speed (1-min. avg.)',
        'unit':'m/s',
        'lb':0,
        'plot_range':2*24,
        'interval':INTERVAL,
    },
    {
        'dbtag':'d',
        'description':'Wind direction (1-min. avg.)',
        'unit':'Deg',
        'lb':0,
        'ub':360,
        'plot_range':2*24,
        'interval':INTERVAL,
    },
    {
        'dbtag':'g',
        'description':'Wind gust (max. in past 1-min)',
        'unit':'m/s',
        'lb':0,
        'plot_range':2*24,
        'interval':INTERVAL,
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
