name = 'Water Level'
location = 'Marine Corps Base Hawaii'
note = 'Ultrasonic tide gauge (cellular; 0.5~10m). Hardware v0.6, firmware 20210924'
#tags = ['tide gauge', 'cellular', 'MB7388', '181m179s']
latitude = 21.434098
longitude = -157.757516
deployment_status = 'staging'

coreid = '360031000251383133363636'

INTERVAL_S = 12*60

conf = [
    {
        'dbtag':'ts',
        'description':'Sample time (Device clock)',
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'d2w',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'lb':501,
        'ub':9998,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'std',
        'unit':'mm',
        'description':'Sample standard deviation',
        #'lb':?,
        #'ub':?,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'Vb',
        'unit':'V',
        'description':'Battery voltage',
        'lb':3.7,
        'ub':4.2,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'SoC',
        'unit':'%',
        'description':'State of Charge',
        'lb':40,
        'ub':100,
        'interval':10*INTERVAL_S,
        'plot':False,
    },
    {
        'dbtag':'sc',
        #'dbtype':'INT',
        'description':'# of measurements within 3σ',
        'lb':30,
        'ub':60,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'comm_error_count',
        'dbtype':'INT',
        'description':'Sensor communication error count',
        'lb':0,
        'ub':6,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'no_target_count',
        'dbtype':'INT',
        'description':'Number of no-target pings since the last transmission',
        'lb':0,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'battery_state',
        'dbtype':'INT',
        'description':'2: charging; 3: charged; 4: discharging; 5: fault; 0: unknown',
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'uptime',
        'description':'Time spent awake since last reset',
        'unit':'seconds',
        'lb':10*60,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'publish_retry_count',
        'dbtype':'INT',
        'description':'Number of transmission attempts',
        'lb':0,
        'ub':3,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'fault_count',
        'dbtype':'INT',
        'description':'Fault count',
        'lb':0,
        'ub':7,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'reset_reason',
        'dbtype':'INT',
        'description':'20: button/uC; 40: power; 70: OTA update; 130:panic; 140: self',
        'lb':0,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'n_idle',
        'dbtype':'INT',
        'description':'Length of IDLE phase',
        'unit':'seconds',
        'lb':0,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'n_active',
        'dbtype':'INT',
        'description':'Length of ACTIVE phase',
        'unit':'seconds',
        'lb':1,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'n_repeat',
        'dbtype':'INT',
        'description':'Number of cycles per uC session',
        'lb':1,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'sps',
        'dbtype':'INT',
        'description':'Ultrasonic ping per second',
        'lb':1,
        'interval':INTERVAL_S,
    },
    {
        'dbtag':'n_tx_group',
        'dbtype':'INT',
        'description':'Number of uC sessions to execute per transmission',
        'lb':1,
        'interval':INTERVAL_S,
    },
]


if '__main__' == __name__:
    for c in conf:
        print('- - -')
        for k, v in c.items():
            print(k, ':' ,v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf, basename(__file__).split('.')[0].replace('_', '-'))
