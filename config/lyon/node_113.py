name = 'Heater Controller'
location = 'Lyon Arboretum'
google_earth_link = '#'
note = '-'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC4IAGIJjwLEyy9SN71MW08UXmMqS8dkuURGyBX1xjiFiYUrIySkec7oxf9JMXU4d2PmIWpqpUqXKOh5JN90HK60R6Ip3PohnoGqyNIBrNKOD/iHpmSh/MmgyyMYKkmC7my6pR/xHFcUx9ITyHExIWbe2H4KMw8K12VZWyVLooVC5djH3mmtdLx7iZqy0xLK3K+LA4ByP4isxP0ToKN4/ykMpQ5G/hSPDG37gy5Ps3PiDR6dDDPRXLUF5RiFJWlhvdPaRXPL5L27rfPyXGsRppzEsi1MusW8691Iamg+E5s3Gd4bscq9MKsUGRTA5Ko8pyvjCgWxxWs+9zmHhIzkfxv pi@node-113'
latitude = 21.333127
longitude = -157.801550


conf = [
    {
        'dbtag':'ts',
        'description':'Time of sampling',
        'plot':False,
        'interval':60,
    },
    {
        'dbtag':'t0',
        'unit':'Deg.C',
        'description':'CH0 feedback (heater temperature)',
        'interval':60,
        'lb':10,
        'ub':40,
        'plot':False,
    },
    {
        'dbtag':'t1',
        'unit':'Deg.C',
        'description':'CH1 feedback (heater temperature)',
        'interval':60,
        'lb':10,
        'ub':40,
        'plot':False,
    },
    {
        'dbtag':'t2',
        'unit':'Deg.C',
        'description':'CH2 feedback (heater temperature)',
        'interval':60,
        'lb':10,
        'ub':40,
        'plot':False,
    },
    {
        'dbtag':'t3',
        'unit':'Deg.C',
        'description':'CH3 feedback (heater temperature)',
        'interval':60,
        'lb':10,
        'ub':40,
        'plot':False,
    },
    {
        'dbtag':'t4',
        'unit':'Deg.C',
        'description':'CH4 feedback (heater temperature)',
        'interval':60,
        'lb':10,
        'ub':40,
        'plot':False,
    },
    # - - -
    {
        'dbtag':'s0',
        'unit':'-',
        'description':'CH0 PID output',
        'interval':60,
        'lb':-10,
        'ub':10,
    },
    {
        'dbtag':'s1',
        'unit':'-',
        'description':'CH1 PID output',
        'interval':60,
        'lb':-10,
        'ub':10,
    },
    {
        'dbtag':'s2',
        'unit':'-',
        'description':'CH2 PID output',
        'interval':60,
        'lb':-10,
        'ub':10,
    },
    {
        'dbtag':'s3',
        'unit':'-',
        'description':'CH3 PID output',
        'interval':60,
        'lb':-10,
        'ub':10,
    },
    {
        'dbtag':'s4',
        'unit':'-',
        'description':'CH4 PID output',
        'interval':60,
        'lb':-10,
        'ub':10,
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
