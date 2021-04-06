name = 'Rainfall'
location = 'Coast Guard Tower, He\'eia Fishpond'
note = 'Bucket rain gauge (XBee). Firmware rain0.1, hardware v0.2.'
latitude = 21.434779
longitude = -157.805064


conf = [
    {
        'dbtag':'ts',
        'description':'Sample time',
        'interval':60*60,
        'plot_range': 7*24,
    },
    {
        'dbtag':'mm',
        'unit':'mm/hr',
        'description':'Hourly rain fall',
        'lb':0,
        'ub':433,   # annual average
        'interval':60*60,
        'plot_range': 3*30*24,
    },
    {
        'dbtag':'Vb',
        'unit':'V',
        'description':'Battery voltage',
        'lb':3.7,
        'ub':5.5,
        'interval':60*60,
        'plot_range': 7*24,
    },
    {
        'dbtag':'Vs',
        'unit':'V',
        'description':'Solar panel voltage',
        'lb':0,
        'ub':7.5,
        'interval':60*60,
        'plot_range': 7*24,
    },
    {
        'dbtag':'tc',
        'unit':'-',
        'description':'Tip count (all-time cumulative)',
        'lb':0,
        'interval':60*60,
        'plot_range': 3*30*24,
    },
    {
        'dbtag':'idx',
        'unit':'-',
        'description':'Sample index',
        'lb':2*24,
        'interval':60*60,
        'plot_range': 7*24,
    },
]


if '__main__' == __name__:
    for c in conf:
        print('- - -')
        for k, v in c.items():
            print(k, ':' ,v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf, basename(__file__).split('.')[0].replace('_', '-'))
