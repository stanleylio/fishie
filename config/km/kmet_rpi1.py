subscribeto = ['166.122.96.12:9002','166.122.96.98:9002']
#private_key_file = '/home/pi/.ssh/id_rsa'
#data_dir = '/var/kmetlog/data'
#log_dir = '/var/kmetlog/log'
#service_discovery_port = 9005
log2txt_output_path = '/var/kmetlog/data'

public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDT+oyHraN+uigppjBTb+9C0PMxzA1YPUyeBQ0Xf348pKINvgS4qrVKiee8zftoNx7TX6g1RjK/vObtY+xuFUJ1XfVOe4BmywDwcUNVwhBHyyyqpqs+BL3ggAy2XzDa6JrsGt2iPqmf/kXS3nJWRisfhZEXYPfWQfilDdm21tYcVRyslgbFSvSYMWhUpSXMmnyhj+RpPxbsgNTUFV9A7fVhmhBXnM1GmzftwE9v7nyonQJuXDprFb059yYLhZ0vbeHlQ2pCsEDcdMBdanZGvwByWjLmXI8a1vLZUXVsEMicjoy8KQ5l/SwVdjp/Z57w64BEUsvE8rX+X+YJTsVuWeP5 pi@kmet-rpi1'

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
        
