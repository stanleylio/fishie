# -*- coding: utf-8 -*-
name = 'Taro Patch'
location = '(TBD)'
note = 'Cellular stream gauge. Each sample is average of 5 measurements taken every 60 seconds. One transmission every 2 samples. Firmware v0.2, hardware v0.2.'

coreid = '2c0024000f51363034323832'


conf = [
    {
        'dbtag':'ts',
        'description':'Sample time (Electron clock)',
        'interval':10*60,
    },
    {
        'dbtag':'Pa',
        'unit':'kPa',
        'description':'Barometric pressure (BME280)',
        'lb':80,
        'ub':120,
        'interval':10*60,
    },
    {
        'dbtag':'Ta',
        'unit':'Deg.C',
        'description':'Air temperature (BME280)',
        'lb':10,
        'ub':50,
        'interval':10*60,
    },
    {
        'dbtag':'RH',
        'unit':'%',
        'description':'% Relative humidity (BME280)',
        'lb':0,
        'ub':100,
        'interval':10*60,
    },
    {
        'dbtag':'Pw',
        'unit':'kPa',
        'description':'Water pressure (MS5803)',
        'lb':80,
        'ub':160,
        'interval':10*60,
    },
    {
        'dbtag':'Tw',
        'unit':'Deg.C',
        'description':'Water temperature (MS5803)',
        'lb':10,
        'ub':50,
        'interval':10*60,
    },
    {
        'dbtag':'ssa',
        'description':'# of valid measurements in mean calculation (BME280)',
        'lb':1,
        'ub':5,
        'interval':10*60,
    },
    {
        'dbtag':'ssw',
        'description':'# of valid measurements in mean calculation (MS5803)',
        'lb':1,
        'ub':5,
        'interval':10*60,
    },
    {
        'dbtag':'VbattV',
        'unit':'V',
        'description':'Battery voltage',
        'lb':3.7,
        'ub':5.5,
        'interval':10*60,
    },
    {
        'dbtag':'SoC',
        'unit':'%',
        'description':'State of Charge',
        'lb':30,
        'ub':100,
        'interval':10*60,
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
