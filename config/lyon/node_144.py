name = 'Logger'
location = 'Lyon Arboretum'
google_earth_link = '#'
note = '(TBD)'
public_key = ''
latitude = 21.333127
longitude = -157.801550


conf = [
    {
        'dbtag':'ts',
        'description':'Time of sampling',
        'plot':True,
        'interval':60,
    },
    {
        'dbtag':'t0',
        'unit':'Deg.C',
        'description':'TSYS01 (CH0 0x77)',
        'interval':60,
        'lb':10,
        'ub':40,
        'plot':False,
    },
    {
        'dbtag':'t1',
        'unit':'Deg.C',
        'description':'TSYS01 (CH1 0x77, depth at 60 cm)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t2',
        'unit':'Deg.C',
        'description':'TSYS01 (CH2 0x77, depth at 60 cm)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t3',
        'unit':'Deg.C',
        'description':'TSYS01 (CH3 0x77, depth at 20 cm)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t4',
        'unit':'Deg.C',
        'description':'TSYS01 (CH4 0x77, depth at 40 cm)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t5',
        'unit':'Deg.C',
        'description':'TSYS01 (CH5 0x77, depth at 80 cm)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t6',
        'unit':'Deg.C',
        'description':'TSYS01 (CH6 0x77, depth at 80 cm)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t7',
        'unit':'Deg.C',
        'description':'TSYS01 (CH7 0x77)',
        'interval':60,
        'lb':10,
        'ub':40,
        'plot':False,
    },
# - - -
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
        'description':'Remaining free disk space',
        'lb':800,
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
