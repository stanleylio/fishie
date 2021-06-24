name = 'controller21'
location = 'Coconut Island'
note = "v0 code: {'neutral':0, 'heating':1, 'cooling':2, 'flush':3}"
latitude = 21.4347
longitude = -157.7990
deployment_status = 'deployed'

conf = [
    {
        'dbtag':'ts',
        'description':'Device clock',
        'interval':60,
    },
    {
        'dbtag':'t0',
        'unit':'\u00b0C',
        'description':'Water Temperature',
        'lb':22,
        'ub':35,
        'interval':60,
        'plot_range':14*24,
    },
    {
        'dbtag':'c0',
        'unit':'\u00b0C',
        'description':'Probe offset',
        'lb':-1,
        'ub':1,
        'interval':60,
        'plot_range':14*24,
    },
    {
        'dbtag':'s0',
        'unit':'\u00b0C',
        'description':'Setpoint',
        'lb':0,
        'ub':50,
        'interval':60,
        'plot_range':14*24,
    },
    {
        'dbtag':'v0',
        'unit':'-',
        'description':'Valve state',
        'interval':60,
        'plot_range':14*24,
    },
    {
        'dbtag':'k',
        'unit':'-',
        'description':'Tank number',
        'interval':60,
        'plot_range':14*24,
    },
    {
        'dbtag':'uptime_second',
        'description':'Uptime in seconds',
        'lb':24*60*60,
        'interval':60,
        'plot_range':2*24,
    },
    {
        'dbtag':'freeMB',
        'unit':'MB',
        'description':'Remaining free disk space',
        'lb':800,
        'interval':60,
        'plot_range':2*24,
    },
    {
        'dbtag':'cpu_temp',
        'unit':'\u00b0C',
        'description':'CPU Temperature',
        'lb':5,
        'ub':68,
        'interval':60,
        'plot_range':2*24,
    },
]


if '__main__' == __name__:
    for c in conf:
        print('- - -')
        for k,v in c.items():
            print(k,':',v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf,basename(__file__).split('.')[0].replace('_','-'))
