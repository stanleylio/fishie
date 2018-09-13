# -*- coding: utf-8 -*-
name = '"Cromulent"'
location = '(TBD)'
note = 'Chlorophyll and Turbidity (cellular FLNTUS)'

#coreid = ''

conf = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE NOT NULL',
        'description':'FLNTUS Time',
        'plot':True,
        'interval':12*60,
    },
    {
        'dbtag':'C',
        'description':'Chlorophyll (EX/EM: 470/695nm)',
        'unit':'mg/L',
        'lb':0,
        'ub':0.0121*(4130 - 46),
        'plot_range':7*24,
        'interval':12*60,
    },
    {
        'dbtag':'N',
        'description':'Turbidity (700nm)',
        'unit':'NTU',
        'lb':0,
        'ub':0.0061*(4130 - 50),
        'plot_range':7*24,
        'interval':12*60,
    },
    {
        'dbtag':'ch695',
        'description':'Chlorophyll raw count (695nm)',
        'unit':'-',
        'lb':0,
        'ub':4130,
        'plot_range':7*24,
        'interval':12*60,
    },
    {
        'dbtag':'ch700',
        'description':'Turbidity raw count (700nm)',
        'unit':'-',
        'lb':0,
        'ub':4130,
        'plot_range':7*24,
        'interval':12*60,
    },
    {
        'dbtag':'Vb',
        'unit':'V',
        'description':'Battery voltage',
        'lb':3.7,
        'ub':5.5,
        'interval':12*60,
    },
    {
        'dbtag':'SoC',
        'unit':'%',
        'description':'State of Charge',
        'lb':30,
        'ub':100,
        'interval':12*60,
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
