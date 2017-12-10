# -*- coding: utf-8 -*-
name = 'MSB Meteorological Station'
location = 'Marine Science Building Rooftop'
note = 'BME280 and RM Young 05106. 10Hz wind direction and 1Hz wind speed display; logged once a minute. Pi cape v0.3 with WDT.'


INTERVAL = 60
NGROUP = 7


conf = [
    {
        'dbtag':'Timestamp',
        'dbtype':'DOUBLE NOT NULL',
        'description':'Time of sampling',
        'plot':False,
        'interval':60,
    },
    {
        'dbtag':'wind_mps',
        'description':'Wind speed (1-min. avg.)',
        'unit':'m/s',
        'lb':0,
        'plot_range':2*24,
        'interval':60,
    },
    {
        'dbtag':'wind_dir_deg',
        'description':'Wind direction (1-min. avg.)',
        'unit':'Deg',
        'lb':0,
        'ub':360,
        'plot_range':2*24,
        'interval':60,
    },
    {
        'dbtag':'wind_gust_mps',
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
    {
        'dbtag':'rain_bucket_tipped',
        'description':'Time when the TR-525I bucket tipped',
        'lb':0,
        'interval':365*24*60*60,    # at least rain once a year?
    },
    {
        'dbtag':'rain_hourly_count',
        'description':'Hourly tip count',
        'lb':0,
        'ub':3600,
        'interval':60*60,
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
