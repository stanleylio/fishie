# -*- coding: utf-8 -*-
name = 'Coral Tank Module 1'
location = 'Coconut Island'
note = 'Temperature Control Demo'


conf = [
    {
        'dbtag':'t0',
        'unit':'Deg.C',
        'description':'Tank #1 Water Temperature',
        'lb':22,
        'ub':31,
        'interval':60,
    },
    {
        'dbtag':'t1',
        'unit':'Deg.C',
        'description':'Tank #2 Water Temperature',
        'lb':22,
        'ub':31,
        'interval':60,
    },
    {
        'dbtag':'t2',
        'unit':'Deg.C',
        'description':'Tank #3 Water Temperature',
        'lb':22,
        'ub':31,
        'interval':60,
    },
    {
        'dbtag':'t3',
        'unit':'Deg.C',
        'description':'Tank #4 Water Temperature',
        'lb':22,
        'ub':31,
        'interval':60,
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
