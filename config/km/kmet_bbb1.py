subscribeto = ['localhost:9011', 'localhost:9012', 'localhost:9013', 'localhost:9014', 'localhost:9015']
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDQdchxRE7jkBOEwPQrPXAy9amx8jiuWZcqfC+uB5APAKcVxf9ih3BkTRcyDKY6TY4njWptYMYhsfaNfId+IEJGZ+SWMgCb1hS3AY3MgXi97ti6cBCuJzT8QTGFj2JCmgJLTiK75gtliOs8YhDoK7Q8wHcUDRrI+Xfo64g/v6h5f86pUN6hLng7lm9HWANWgoAc5UPdUpMfJ7vH9BBv1saAZhhjo5RhDz5E2Ea8m9U2DzV1cDeaJQ5Vdykl/kZLt8p3I7izd8smLA5baNdrDbwfu/ARjzrVuhiZkt1KxcnmNTE0ueqHyc4u9xp1hUCwdWBW7VLHZ2xCZOJJ2bm3oKzb root@kmet-bbb1'

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
        
