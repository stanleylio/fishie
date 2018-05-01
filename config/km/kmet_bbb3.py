subscribeto = ['localhost:9011', 'localhost:9012', 'localhost:9013', 'localhost:9014', 'localhost:9015']
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCh3IJRLtb1GqdLDRVP1z9GGocb5YsugkquPqa1Rf9J/0btLxoWNZjv++Q6Fjl2U3zKfknKeutuJWDabgDCy1445iHIf5qml6MLc9G1iG/PRhJ8ubx5x6RUBdZY/ULELD7a1opseyjcZ7C4pmHWv8cJNpyEe3GhV2x5jBTzB1EbYHN00qur6o4JLgZCcB43ves9TwsLh45is+6lNgoAhbf8M0bt2LNRakdDXfOUQMNGveSkf6GgfoLvSKqILtUhsJCnJfAC6Nr8k3tf+hT34kBvGR6sWwD2OYsYL/oNjFDAvxpRaAJfoylyWn8l+2PrQsIv6UYvh5YioQ9Kyt/u4O2d root@beaglebone'

DAQ_CH_MAP = {'PIR_mV':3,
              'PIR_case_V':4,
              'PIR_dome_V':5,
              'PSP_mV':0,
              'PAR_V':0,
              'BucketRain_accumulation_mm':2,
              'Rotronics_T_C':6,
              'Rotronics_RH_percent':7,
              'RMYRTD_T_C':1,
              'Rotronics_Fan_rpm':0,
              'RMYRTD_Fan_rpm':1,
              }

'''conf = {}

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
'''


if '__main__' == __name__:
    import sys
    from os.path import expanduser
    sys.path.append(expanduser('~'))
    from node.storage.storage2 import create_table

    for table in conf:
        print(table)
        create_table(conf[table], table, dbname='kmetlog')
        
