# -*- coding: utf-8 -*-
name = 'MSB RPi Met.'
location = 'Roof of MSB, UHM'
note = 'RPi-based Meteological Station'


conf = [
    {
        'dbtag':'ReceptionTime',
        'dbtype':'DOUBLE NOT NULL',
        'description':'Sample time',
        'plot':False,
    },
    {
        'dbtag':'ambient_temperature_bmp',
        'dbtype':'DOUBLE',
        'unit':'Deg.C',
        'description':'Ambient Temperature (BMP180)',
    },
    {
        'dbtag':'ambient_temperature_htu',
        'dbtype':'DOUBLE',
        'unit':'Deg.C',
        'description':'Ambient Temperature (HTU21D)',
    },
    {
        'dbtag':'ground_temperature',
        'dbtype':'DOUBLE',
        'unit':'Deg.C',
        'description':'Ground temperature (DS18B20)',
    },
    {
        'dbtag':'air_quality',
        'dbtype':'DOUBLE',
        'description':'Air Quality',
    },
    {
        'dbtag':'air_pressure',
        'dbtype':'DOUBLE',
        'unit':'hPa',
        'description':'Barometric Pressure',
    },
    {
        'dbtag':'humidity',
        'dbtype':'DOUBLE',
        'unit':'%',
        'description':'Humidity',
    },
    {
        'dbtag':'wind_direction',
        'dbtype':'DOUBLE',
        'unit':'Degree',
        'description':'Wind Direction',
    },
    {
        'dbtag':'wind_speed',
        'dbtype':'DOUBLE',
        'unit':'knot',
        'description':'Wind Speed',
    },
    {
        'dbtag':'wind_gust',
        'dbtype':'DOUBLE',
        'unit':'knot',
        'description':'Wind Gust',
    },
    {
        'dbtag':'rainfall',
        'dbtype':'DOUBLE',
        'unit':'mm/hr',
        'description':'Rainfall',
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

