name = 'Waikalua Anemometer'
location = 'Waikalua, Kāneʻohe Bay, Oahu'
note = '10Hz wind direction and 1Hz wind speed display; logged once a minute. Pi cape v0.3 with WDT.'
time_col = 'ReceptionTime'


INTERVAL = 60
NGROUP = 7


conf = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE NOT NULL',
        'description':'Time of sampling',
        'plot':False,
        'interval':60,
    },
    {
        'dbtag':'v',
        'description':'Wind speed (1-min. avg.)',
        'unit':'m/s',
        'lb':0,
        'plot_range':2*24,
        'interval':60,
    },
    {
        'dbtag':'d',
        'description':'Wind direction (1-min. avg.)',
        'unit':'Degree',
        'lb':0,
        'ub':360,
        'plot_range':2*24,
        'interval':60,
    },
    {
        'dbtag':'g',
        'description':'Wind gust (max. in past 1-min)',
        'unit':'m/s',
        'lb':0,
        'plot_range':2*24,
        'interval':60,
    },
    {
        'dbtag':'uptime_second',
        'description':'Uptime in seconds',
        'lb':24*60*60,
        'interval':60,
    },
    {
        'dbtag':'freeMB',
        'unit':'MB',
        'description':'Free disk space',
        'lb':2000,
        'interval':60,
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
