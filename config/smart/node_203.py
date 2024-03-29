name = 'Palolo Rainfall (St Louis)'
location = 'Saint Louis School, Oahu, HI'
note = 'Rain. Solar, Arduino + XBee'
latitude = 21.28909
longitude = -157.80499

conf = [
    {
        'dbtag':'ts',
        'description':'Time of sampling',
        'plot':True,
        'interval':60*60,
    },
    {
        'dbtag':'rain_bucket_tipped',
        'unit':'-',
        'description':'-',
        'lb':1,
        'plot_range':7*24,
        'interval':365*24*60*60,    # gotta tip at least once a year?
    },
    {
        'dbtag':'mm',
        'unit':'mm/hr',
        'description':'Accumulated per-hour',
        'lb':0,
        'plot_range':7*24,
        'interval':60*60,
    },
    {
        'dbtag':'da',
        'unit':'mm/day',
        'description':'Accumulated per-day',
        'lb':0,
        'plot_range':7*24,
        'interval':24*60*60,
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
