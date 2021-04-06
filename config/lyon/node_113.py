name = '5-channel Thermostat'
location = 'Lyon Arboretum'
google_earth_link = '#'
note = 'Soil Warming'
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
        'dbtag':'pv0',
        'unit':'Deg.C',
        'description':'Heater #0 temperature',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'pv1',
        'unit':'Deg.C',
        'description':'Heater #1 temperature',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'pv2',
        'unit':'Deg.C',
        'description':'Heater #2 temperature',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'pv3',
        'unit':'Deg.C',
        'description':'Heater #3 temperature',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'pv4',
        'unit':'Deg.C',
        'description':'Heater #4 temperature',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    # - - -
    {
        'dbtag':'sp0',
        'unit':'-',
        'description':'CH0 setpoint',
        'interval':60,
        'lb':-10,
        'ub':35,
    },
    {
        'dbtag':'sp1',
        'unit':'-',
        'description':'CH1 setpoint',
        'interval':60,
        'lb':-10,
        'ub':35,
    },
    {
        'dbtag':'sp2',
        'unit':'-',
        'description':'CH2 setpoint',
        'interval':60,
        'lb':-10,
        'ub':35,
    },
    {
        'dbtag':'sp3',
        'unit':'-',
        'description':'CH3 setpoint',
        'interval':60,
        'lb':-10,
        'ub':35,
    },
    {
        'dbtag':'sp4',
        'unit':'-',
        'description':'CH4 setpoint',
        'interval':60,
        'lb':-10,
        'ub':35,
    },
    # - - -
    {
        'dbtag':'s0',
        'unit':'-',
        'description':'CH0 PID output',
        'interval':60,
        'lb':-10,
        'ub':10,
        'plot':False,
    },
    {
        'dbtag':'s1',
        'unit':'-',
        'description':'CH1 PID output',
        'interval':60,
        'lb':-10,
        'ub':10,
        'plot':False,
    },
    {
        'dbtag':'s2',
        'unit':'-',
        'description':'CH2 PID output',
        'interval':60,
        'lb':-10,
        'ub':10,
        'plot':False,
    },
    {
        'dbtag':'s3',
        'unit':'-',
        'description':'CH3 PID output',
        'interval':60,
        'lb':-10,
        'ub':10,
        'plot':False,
    },
    {
        'dbtag':'s4',
        'unit':'-',
        'description':'CH4 PID output',
        'interval':60,
        'lb':-10,
        'ub':10,
        'plot':False,
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
