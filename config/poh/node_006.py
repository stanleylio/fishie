# -*- coding: utf-8 -*-
name = 'Wind Monitor'
location = 'Coast Guard Tower, He\'eia Fishpond'
note = 'RM Young 05106 Anemometer (2.4GHz)'
latitude = 21.434779
longitude = -157.805064


INTERVAL = 60


conf = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE NOT NULL',
        'description':'Time of sampling',
        'plot':True,
        'interval':INTERVAL,
    },
    {
        'dbtag':'v',
        'description':'Wind speed',
        'unit':'m/s',
        'plot_range':7*24,
        'lb':0,
        'interval':INTERVAL,
    },
    {
        'dbtag':'d',
        'description':'Wind direction (1-min. avg.)',
        'unit':'Deg',
        'plot_range':7*24,
        'lb':0,
        'ub':360,
        'interval':INTERVAL,
    },
    {
        'dbtag':'g',
        'description':'Wind gust (max. in past 1-min)',
        'unit':'m/s',
        'lb':0,
        'plot_range':7*24,
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
