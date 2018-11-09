# -*- coding: utf-8 -*-
name = 'Lyon Greenhouse Weather Station'
location = 'Lyon Arboretum'
note = 'Yinphan and Yu-Fen\'s CR3000 meteorological station at Lyon Arboretum'

coreid = '7JkkKNm75mh3EZiQVkw9kjJB'


INTERVAL = 15*60


conf = [
    {
        'dbtag':'ts',
        'description':'Sample time (device clock, converted from HST to UTC)',
        'interval':INTERVAL,
    },
    {
        'dbtag':'SWup_Avg',
        'unit':'W/m^2',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'SWdn_Avg',
        'unit':'W/m^2',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'LWup_Avg',
        'unit':'W/m^2',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'LWdn_Avg',
        'unit':'W/m^2',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'Trnet_Avg',
        'unit':'-',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'Tair_1_Avg',
        'unit':'Deg.C',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'RH_1_Avg',
        'unit':'%',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'Tair_2_Avg',
        'unit':'Deg.C',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'RH_2_Avg',
        'unit':'%',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'WindSpeed',
        'unit':'m/s',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'WindSpeed_rs',
        'unit':'m/s',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'WindDir',
        'unit':'Deg',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'WindDir_sd',
        'unit':'Deg',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'WindDir_uv',
        'unit':'Deg',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'Tsoil_Avg',
        'unit':'Deg.C',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'SoilHeatFlux_Avg_1_',
        'unit':'W/m^2',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'SoilHeatFlux_Avg_2_',
        'unit':'W/m^2',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'SoilMoisture_Avg_1_',
        'unit':'m^3/m^3',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'SoilMoisture_Avg_2_',
        'unit':'m^3/m^3',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'SoilMoisture_Avg_3_',
        'unit':'m^3/m^3',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'SM_us_Avg_1_',
        'unit':'µs',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'SM_us_Avg_2_',
        'unit':'µs',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'SM_us_Avg_3_',
        'unit':'µs',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'SoilMoisture_T_Avg',
        'unit':'m^3/m^3',
        'description':'-',
        'interval':INTERVAL,
    },
    {
        'dbtag':'Rainfall_Tot',
        'unit':'mm',
        'description':'-',
        'interval':INTERVAL,
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
