name = 'MSB Meteorological Station'
location = 'Marine Science Building Rooftop'
note = 'BME280 and RM Young 05106. 10Hz wind direction and 1Hz wind speed display; logged once a minute. Pi cape v0.3 with WDT.'
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
        'unit':'°C',
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
        'lb':15,
        'ub':85,
        'plot_range':7*24,
        'interval':60,
    },
    {
        'dbtag':'P_ext',
        'unit':'kPa',
        'description':'Barometric pressure (BME280)',
        'lb':80,
        'ub':120,
        'plot':False,
        'interval':60,
    },
    {
        'dbtag':'T_ext',
        'unit':'°C',
        'description':'Air temperature',
        'lb':-10,
        'ub':60,
        'plot_range':7*24,
        'interval':60,
    },
    {
        'dbtag':'RH_ext',
        'unit':'%',
        'description':'% Relative humidity (BME280)',
        'lb':15,
        'ub':85,
        'plot':False,
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
        'lb':24*60*60,
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
        'lb':2000,
        'interval':60,
    },
    {
        'dbtag':'VbattV',
        'unit':'V',
        'description':'12V supply voltage',
        'lb':11,
        'ub':14,
        'interval':60,
    },
    {
        'dbtag':'rain_bucket_tipped',
        'description':'Time when the TR-525I bucket tipped',
        'lb':0,
        'plot':False,
        'interval':365*24*60*60,    # at least rain once a year?
    },
    {
        'dbtag':'rain_hourly_count',
        'description':'Hourly tip count',
        'lb':0,
        'ub':3600,
        'plot':False,
        'interval':60*60,
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
