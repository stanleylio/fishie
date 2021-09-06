name = 'rain-box-3'
location = '(TBD)'
note = "-"
#latitude = 21.4347
#longitude = -157.7990
deployment_status = 'staging'

coreid = '013298498FA9DFAE'

conf = [
    {
        'dbtag':'analog_in_1',
        'unit':'mm/m',
        'description':'rain',
        'lb':0,
        'interval':60*60,
    },
    {
        'dbtag':'temperature_1',
        'unit':'°C',
        'description':'Temperature',
        'lb':5,
        'ub':60,
        'interval':60*60,
    },
    {
        'dbtag':'voltage_1',
        'unit':'V',
        'description':'Battery voltage',
        'lb':3.3,
        'ub':5.0,
        'interval':60*60,
    },
    {
        'dbtag':'digital_out_1',
        'description':'running software version',
        'interval':60*60,
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
