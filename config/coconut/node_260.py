name = 'Octo-TSYS'
location = 'Coral Resilience Lab, HIMB'
note = '(TBD)'
#latitude = 21.333127
#longitude = -157.801550

conf = [
    {
        'dbtag':'idx',
        'description':'Sample index',
        'lb':24*60*60/(1*60),
        'interval':60,
    },
    {
        'dbtag':'ticker',
        'description':'1 Hz ticker',
        'lb':24*60*60,
        'interval':60,
    },
    {
        'dbtag':'Vb',
        'description':'Battery voltage',
        'lb':3.5,
        'ub':4.3,
        'interval':60,
    },
    {
        'dbtag':'Vs',
        'description':'Solar panel voltage',
        'lb':0,
        'ub':7.5,
        'interval':60,
    },
    {
        'dbtag':'t0',
        'unit':'Deg.C',
        'description':'(TBD)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t1',
        'unit':'Deg.C',
        'description':'(TBD)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t2',
        'unit':'Deg.C',
        'description':'(TBD)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t3',
        'unit':'Deg.C',
        'description':'(TBD)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t4',
        'unit':'Deg.C',
        'description':'(TBD)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t5',
        'unit':'Deg.C',
        'description':'(TBD)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t6',
        'unit':'Deg.C',
        'description':'(TBD)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t7',
        'unit':'Deg.C',
        'description':'(TBD)',
        'interval':60,
        'lb':10,
        'ub':40,
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
