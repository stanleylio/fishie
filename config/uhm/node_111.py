name = '"Because-I-Can"'
location = 'MSB, UH Manoa'
google_earth_link = '#'
note = 'Experimental NodeMCU-based 8T-chain'
public_key = ''


conf = [
    {
        'dbtag':'t1',
        'unit':'Deg.C',
        'description':'TSYS01 (CH0 0x76)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t2',
        'unit':'Deg.C',
        'description':'TSYS01 (CH0 0x77)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t3',
        'unit':'Deg.C',
        'description':'TSYS01 (CH1 0x76)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t4',
        'unit':'Deg.C',
        'description':'TSYS01 (CH1 0x77)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t5',
        'unit':'Deg.C',
        'description':'TSYS01 (CH2 0x76)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t6',
        'unit':'Deg.C',
        'description':'TSYS01 (CH2 0x77)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t7',
        'unit':'Deg.C',
        'description':'TSYS01 (CH3 0x76)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'t8',
        'unit':'Deg.C',
        'description':'TSYS01 (CH3 0x77)',
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
