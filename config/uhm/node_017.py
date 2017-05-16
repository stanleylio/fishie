# -*- coding: utf-8 -*-
name = 'MSB RPi Met.'
location = 'Roof of MSB, UHM'
note = 'RPi-based Meteological Station'


conf = [
#    {
#        'dbtag':'ReceptionTime',
#        'dbtype':'DOUBLE NOT NULL',
#        'description':'Sample time',
#        'plot':False,
#    },
    {
        'dbtag':'ambient_temperature_bmp',
        'unit':'Deg.C',
        'description':'Ambient Temperature (BMP180)',
    },
    {
        'dbtag':'ambient_temperature_htu',
        'unit':'Deg.C',
        'description':'Ambient Temperature (HTU21D)',
    },
    {
        'dbtag':'ground_temperature',
        'unit':'Deg.C',
        'description':'Ground temperature (DS18B20)',
    },
    {
        'dbtag':'air_quality',
        'description':'Air Quality',
    },
    {
        'dbtag':'air_pressure',
        'unit':'hPa',
        'description':'Barometric Pressure',
    },
    {
        'dbtag':'humidity',
        'unit':'%',
        'description':'Humidity',
    },
    {
        'dbtag':'wind_direction',
        'unit':'Degree',
        'description':'Wind Direction',
    },
    {
        'dbtag':'wind_speed',
        'unit':'knot',
        'description':'Wind Speed',
    },
    {
        'dbtag':'wind_gust',
        'unit':'knot',
        'description':'Wind Gust',
    },
    {
        'dbtag':'rainfall',
        'unit':'mm/hr',
        'description':'Rainfall',
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table

    conf.insert(0,{'dbtag':'ReceptionTime','dbtype':'DOUBLE NOT NULL'})
    create_table(conf,basename(__file__).split('.')[0].replace('_','-'))
