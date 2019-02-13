name = '(TBD)'
location = '"Greek"'
note = 'WiFi-only node'
public_key = ''
latitude = 21.333127
longitude = -157.801550

coreid = '1c003a001147343438323536'

conf = [
    {
        'dbtag':'ts',
        'description':'Time of sampling',
        'plot':True,
        'interval':60,
    },
    {
        'dbtag':'idx',
        'description':'Sample index',
        'lb':24*60*60/(1*60),
        'interval':60,
    },
    {
        'dbtag':'t0',
        'unit':'Deg.C',
        'description':'TSYS01 (CH0 0x77, depth at X cm)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t1',
        'unit':'Deg.C',
        'description':'TSYS01 (CH1 0x77, depth at X cm)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t2',
        'unit':'Deg.C',
        'description':'TSYS01 (CH2 0x77, depth at X cm)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t3',
        'unit':'Deg.C',
        'description':'TSYS01 (CH3 0x77, depth at X cm)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t4',
        'unit':'Deg.C',
        'description':'TSYS01 (CH4 0x77, depth at X cm)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t5',
        'unit':'Deg.C',
        'description':'TSYS01 (CH5 0x77, depth at X cm)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t6',
        'unit':'Deg.C',
        'description':'TSYS01 (CH6 0x77, depth at X cm)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t7',
        'unit':'Deg.C',
        'description':'TSYS01 (CH7 0x77, depth at X cm)',
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
