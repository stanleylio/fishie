# -*- coding: utf-8 -*-
name = '(TBD)'
location = '(TBD)'
note = '(TBD)'


conf = [
    {
        'dbtag':'Timestamp',
        'description':'Sample time (device clock)',
        'interval':10*60,
    },
    {
        'dbtag':'Temp',
        'unit':'Deg.C',
        'description':'Water temperature',
        'lb':0,
        'ub':50,
        'interval':10*60,
    },
    {
        'dbtag':'SpCond',
        'unit':'mS/cm',
        'description':'Specific conductivity?',
        'lb':0,
        'interval':10*60,
    },
    {
        'dbtag':'Cond',
        'unit':'mS/cm',
        'description':'Conductivity',
        'lb':0,
        'interval':10*60,
    },
    {
        'dbtag':'Sal',
        'unit':'ppt',
        'description':'Salinity',
        'lb':0,
        'ub':40,
        'interval':10*60,
    },
    {
        'dbtag':'Press',
        'unit':'psia',
        'description':'Water pressure',
        'lb':0,
        'ub':203,   # or 14BAR.
        'interval':10*60,
    },
    {
        'dbtag':'Depth',
        'unit':'meter',
        'description':'Water depth',
        'ub':1,
        'interval':10*60,
    },
    {
        'dbtag':'Battery',
        'unit':'volts',
        'description':'YSI battery voltage',
        'lb':8,
        'ub':15,
        'interval':10*60,
    },
    {
        'dbtag':'VbattV',
        'unit':'V',
        'description':'Telemetry dongle battery voltage',
        'lb':2.9,
        'ub':5.5,
        'interval':60*60,
    },
    {
        'dbtag':'ticker',
        'description':'1Hz ticker',
        'lb':0,
        'interval':60*60,
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
