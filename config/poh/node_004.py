# -*- coding: utf-8 -*-
name = '(decommissioned)'
location = 'Hīhīmanu (first mākāhā)'
note = 'Beaglebone-based node, measuring oxygen, temperature and water depth'
latitude = 21.433912
longitude = -157.805338

conf = [
    {
        'dbtag':'ts',
        'description':'Time of sampling (UTC)',
        'plot':True,
    },
    {
        'dbtag':'Pc',
        'unit':'kPa',
        'description':'Barometric pressure (BME280)',
        'lb':90,
        'ub':110,
    },
    {
        'dbtag':'Tc',
        'unit':'Deg.C',
        'description':'Enclosure temperature (BME280)',
        'lb':10,
        'ub':50,
    },
    {
        'dbtag':'RHc',
        'unit':'%RH',
        'description':'Enclosure humidity (BME280)',
        'lb':10,
        'ub':80,
    },
    {
        'dbtag':'Pw',
        'unit':'kPa',
        'description':'Water pressure (MS5803-14BA)',
        'lb':80,
        'ub':150,
    },
    {
        'dbtag':'Tw',
        'unit':'Deg.C',
        'description':'Water temperature (MS5803-14BA)',
        'lb':10,
        'ub':50,
    },
    {
        'dbtag':'T_TSYS01',
        'unit':'Deg.C',
        'description':'Water temperature (TSYS01)',
        'plot':False,
        'lb':-10,
        'ub':50,
    },
    {
        'dbtag':'T_7051',
        'unit':'Deg.C',
        'description':'Water temperature (Si7051)',
        'plot':False,
        'lb':-10,
        'ub':50,
    },
    {
        'dbtag':'O2Concentration',
        'unit':'uM',
        'description':'Oxygen concentration (4330F)',
        'lb':0,
        'ub':450,
    },
    {
        'dbtag':'AirSaturation',
        'unit':'%',
        'description':'Air saturation (4330F)',
        'lb':0,
        'ub':150,
    },
    {
        'dbtag':'Temperature',
        'unit':'Deg.C',
        'description':'Water temperature (4330F)',
        'lb':-20,
        'ub':60,
    },
    {
        'dbtag':'CalPhase',
        'unit':'Deg',
        'description':'CalPhase',
        'plot':False,
    },
    {
        'dbtag':'TCPhase',
        'unit':'Deg',
        'description':'TCPhase',
        'plot':False,
    },
    {
        'dbtag':'C1RPh',
        'unit':'Deg',
        'description':'C1RPh',
        'plot':False,
    },
    {
        'dbtag':'C2RPh',
        'unit':'Deg',
        'description':'C2RPh',
        'plot':False,
    },
    {
        'dbtag':'C1Amp',
        'unit':'mV',
        'description':'C1Amp',
        'plot':False,
    },
    {
        'dbtag':'C2Amp',
        'unit':'mV',
        'description':'C2Amp',
        'plot':False,
    },
    {
        'dbtag':'RawTemp',
        'unit':'mV',
        'description':'RawTemp',
        'plot':False,
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
