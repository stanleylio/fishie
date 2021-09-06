name = 'sonic-1'
location = '(TBD)'
note = "-"
#latitude = 21.4347
#longitude = -157.7990
deployment_status = 'staging'

coreid = '70B3D57ED0044671'

conf = [
    {
        'dbtag':'distance_1',
        'unit':'m',
        'description':'Distance to water surface (top-down)',
        'lb':300,
        'ub':5000,
        'interval':10*60,
    },
    {
        'dbtag':'voltage_1',
        'unit':'V',
        'description':'Battery voltage',
        'lb':3.3,
        'ub':5.0,
        'interval':10*60,
    },
    {
        'dbtag':'digital_out_1',
        'description':'running software version',
        'interval':10*60,
    },
]


if '__main__' == __name__:
    for c in conf:
        print('- - -')
        for k,v in c.items():
            print(k,':',v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf,basename(__file__).split('.')[0].replace('_','-'))
