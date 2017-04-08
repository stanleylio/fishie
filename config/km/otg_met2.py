

conf = {}

tmp = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE PRIMARY KEY', # DOUBLE if not specified
        'description':'Sampling time (POSIX Timestamp)',
    },
    {
        'dbtag':'PIR_mV',
    },
    {
        'dbtag':'PIR_case_V',
    },
    {
        'dbtag':'PIR_dome_V',
    },
]
conf['PIR'] = tmp

tmp = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE PRIMARY KEY',
    },
    {
        'dbtag':'PSP_mV',
    },
]
conf['PSP'] = tmp

tmp = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE PRIMARY KEY',
    },
    {
        'dbtag':'PAR_V',
    },
]
conf['PAR'] = tmp

tmp = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE PRIMARY KEY',
    },
    {
        'dbtag':'UltrasonicWind_apparent_speed_mps',
    },
    {
        'dbtag':'UltrasonicWind_apparent_direction_deg',
    },
]
conf['UltrasonicWind'] = tmp

tmp = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE PRIMARY KEY',
    },
    {
        'dbtag':'OpticalRain_weather_condition',
        'dbtype':'CHAR(2)'      # Not a number!
    },
    {
        'dbtag':'OpticalRain_instantaneous_mmphr',
    },
    {
        'dbtag':'OpticalRain_accumulation_mm',
    },
]
conf['OpticalRain'] = tmp

tmp = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE PRIMARY KEY',
    },
    {
        'dbtag':'BucketRain_accumulation_mm',
    },
]
conf['BucketRain'] = tmp

tmp = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE PRIMARY KEY',
    },
    {
        'dbtag':'Rotronics_T_C',
    },
    {
        'dbtag':'Rotronics_RH_percent',
    },
]
conf['Rotronics'] = tmp

tmp = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE PRIMARY KEY',
    },
    {
        'dbtag':'RMYRTD_T_C',
    },
]
conf['RMYRTD'] = tmp

tmp = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE PRIMARY KEY',
    },
    {
        'dbtag':'BME280_T_C',
    },
    {
        'dbtag':'BME280_P_kPa',
    },
    {
        'dbtag':'BME280_RH_percent',
    },
]
conf['BME280'] = tmp

tmp = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE PRIMARY KEY',
    },
    {
        'dbtag':'RMYRTD_Fan_rpm',
    },
    {
        'dbtag':'Rotronics_Fan_rpm',
    },
]
conf['Misc'] = tmp


#    {
#        'dbtag':'PortWind_apparent_speed_mps',
#    },
#    {
#        'dbtag':'PortWind_apparent_direction_deg',
#    },
#    {
#        'dbtag':'StarboardWind_apparent_speed_mps',
#    },
#    {
#        'dbtag':'StarboardWind_apparent_direction_deg',
#    },


if '__main__' == __name__:
    import sys
    from os.path import expanduser
    sys.path.append(expanduser('~'))
    from node.storage.storage2 import create_table

    for table in conf:
        print(table)
        create_table(conf[table],table,dbname='kmetlog')
        
