# -*- coding: utf-8 -*-
name = 'Cellular test bed'
location = 'UH Manoa'
note = 'Cellular stream gauge. Each sample is average of 5 measurements taken every 60 seconds. One transmission every 2 samples. Firmware v1, hardware v0.2.'

coreid = '410055001951353338363036'


conf = [
    {
        'dbtag':'Timestamp',
        'description':'Sample time (Electron clock)',
        'interval':10*60,
    },
    {
        'dbtag':'P280kPa',
        'unit':'kPa',
        'description':'Barometric pressure (BME280)',
        'lb':80,
        'ub':120,
        'interval':10*60,
    },
    {
        'dbtag':'T280DegC',
        'unit':'Deg.C',
        'description':'Air temperature (BME280)',
        'lb':10,
        'ub':50,
        'interval':10*60,
    },
    {
        'dbtag':'RH280',
        'unit':'%',
        'description':'% Relative humidity (BME280)',
        'lb':0,
        'ub':100,
        'interval':10*60,
    },
    {
        'dbtag':'P5803kPa',
        'unit':'kPa',
        'description':'Water pressure (MS5803)',
        'lb':80,
        'ub':160,
        'interval':10*60,
    },
    {
        'dbtag':'T5803DegC',
        'unit':'Deg.C',
        'description':'Water temperature (MS5803)',
        'lb':10,
        'ub':50,
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
    {
        'dbtag':'sample_size',
        'description':'Number of valid measurements in the group',
        'lb':1,
        'ub':10,
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
