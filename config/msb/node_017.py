# -*- coding: utf-8 -*-
name = 'MSB RPi Met.'
location = 'Roof of MSB, UHM'
note = 'MSB RPi-based Meteological Station'


conf = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE NOT NULL',
        #'comtag':None,
        #'unit':None,
        'description':'Sample time',
        'plot':False,
    },
    {
        'dbtag':'ambient_temperature_bmp',
        'dbtype':'DOUBLE',
        #'comtag':None,
        'unit':'Deg.C',
        'description':'Ambient Temperature (BMP180)',
        #'plot':True,
    },
    {
        'dbtag':'ambient_temperature_htu',
        'dbtype':'DOUBLE',
        'unit':'Deg.C',
        'description':'Ambient Temperature (HTU21D)',
        #'plot':True,
    },
    {
        'dbtag':'ground_temperature',
        'dbtype':'DOUBLE',
        'unit':'Deg.C',
        'description':'Ground temperature (DS18B20)',
        #'plot':True,
    },
    {
        'dbtag':'air_quality',
        'dbtype':'DOUBLE',
        #'unit':None,
        'description':'Air Quality',
        #'plot':True,
    },
    {
        'dbtag':'air_pressure',
        'dbtype':'DOUBLE',
        'unit':'hPa',
        'description':'Barometric Pressure',
        #'plot':True,
    },
    {
        'dbtag':'humidity',
        'dbtype':'DOUBLE',
        'unit':'%',
        'description':'Humidity',
        #'plot':True,
    },
    {
        'dbtag':'wind_direction',
        'dbtype':'DOUBLE',
        'unit':'Degree',
        'description':'Wind Direction',
        #'plot':True,
    },
    {
        'dbtag':'wind_speed',
        'dbtype':'DOUBLE',
        'unit':'knot',
        'description':'Wind Speed',
        #'plot':True,
    },
    {
        'dbtag':'wind_gust',
        'dbtype':'DOUBLE',
        'unit':'knot',
        'description':'Wind Gust',
        #'plot':True,
    },
    {
        'dbtag':'rainfall',
        'dbtype':'DOUBLE',
        'unit':'mm/hr',
        'description':'Rainfall',
        #'plot':True,
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

