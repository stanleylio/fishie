subscribeto = ['localhost:9011', 'localhost:9012', 'localhost:9013', 'localhost:9014', 'localhost:9015']
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC40CPr/EP30b046acfH5hxGLpOFWHnGB9/W7EbnpjX+mbPKXt7wvHcDD2VEV6yjg33+T7skh/z1Aepw2kRtb1B8AO6GjSPNmRSKnWZzXDRuN2SqwefOcmDOfHV6betNrkBbnxcXZyLofhII55ffN0sz4/+pl2Pjq8ot1N0SiTZilgVkHKQxI4d/NjJKKLuDKzgydGYCvEaUDiQoRWkOH52gIsx04u+lD6gtVEJZt7WjJkoJITKAYF4WJG5hoKAIHcRrdrkIqa70Fae1kz/wdjdFI3ZnQmXx82m8G4YsLh0/+IIA8og78NWsj/eRl6G+ykElGW846kPsrbBmUiQ6d2H root@kmet-bbb2'

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

'''conf = [
    {
        'dbtag':'ts',
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
    {
        'dbtag':'PSP_mV',
    },
    {
        'dbtag':'PAR_V',
    },
    {
        'dbtag':'UltrasonicWind_apparent_speed_mps',
    },
    {
        'dbtag':'UltrasonicWind_apparent_direction_deg',
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
    {
        'dbtag':'BucketRain_accumulation_mm',
    },
    {
        'dbtag':'Rotronics_T_C',
    },
    {
        'dbtag':'Rotronics_RH_percent',
    },
    {
        'dbtag':'RMYRTD_T_C',
    },
    {
        'dbtag':'RMYRTD_Fan_rpm',
    },
    {
        'dbtag':'Rotronics_Fan_rpm',
    },
#    {
#        'dbtag':'BME280_T_C',
#    },
#    {
#        'dbtag':'BME280_P_kPa',
#    },
#    {
#        'dbtag':'BME280_RH_percent',
#    },
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
    ]
'''


if '__main__' == __name__:
    import sys
    from os.path import expanduser
    sys.path.append(expanduser('~'))
    from node.storage.storage2 import create_table

    for table in conf:
        print(table)
        create_table(conf[table], table, dbname='kmetlog')
        
