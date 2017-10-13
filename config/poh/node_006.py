# -*- coding: utf-8 -*-
name = 'Windbird'
location = 'First Mākāhā'
note = 'RM Young 05106 Anemometer'


conf = [
    {
        'dbtag':'Timestamp',
        'dbtype':'DOUBLE NOT NULL',
        'description':'Time of sampling',
        'plot':False,
        'plot_range':3*24,
        'interval':1,
    },
    {
        'dbtag':'wind_mps',
        'description':'Wind speed',
        'unit':'m/s',
        'plot_range':3*24,
        'lb':0,
        'interval':1,
    },
    {
        'dbtag':'wind_dir_deg',
        'description':'Wind direction',
        'unit':'Deg',
        'plot_range':3*24,
        'lb':0,
        'ub':360,
        'interval':1,
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
