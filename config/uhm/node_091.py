name = 'T16'
location = 'MSB, UHM'
google_earth_link = '#'
note = 'Tube in a tube in a tube in a tube (TSYS01 stability test)'
public_key = ''

XBEE_PORT = '/dev/ttyUSB0'
XBEE_BAUD = 115200
INTERVAL = 60
NGROUP = 1
XBEELOGDIR = '/var/uhcm/log'


conf = [
    {
        'dbtag':'ts',
        'description':'Time of sampling',
        'plot':False,
        'interval':60,
    },
    {
        'dbtag':'tsys0',
        'unit':'Deg.C',
        'description':'TSYS01 (CH0 0x76)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'tsys1',
        'unit':'Deg.C',
        'description':'TSYS01 (CH0 0x77)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'tsys2',
        'unit':'Deg.C',
        'description':'TSYS01 (CH1 0x76)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'tsys3',
        'unit':'Deg.C',
        'description':'TSYS01 (CH1 0x77)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'tsys4',
        'unit':'Deg.C',
        'description':'TSYS01 (CH2 0x76)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'tsys5',
        'unit':'Deg.C',
        'description':'TSYS01 (CH2 0x77)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'tsys6',
        'unit':'Deg.C',
        'description':'TSYS01 (CH3 0x76)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'tsys7',
        'unit':'Deg.C',
        'description':'TSYS01 (CH3 0x77)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'tsys8',
        'unit':'Deg.C',
        'description':'TSYS01 (CH4 0x76)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'tsys9',
        'unit':'Deg.C',
        'description':'TSYS01 (CH4 0x77)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'tsys10',
        'unit':'Deg.C',
        'description':'TSYS01 (CH5 0x76)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'tsys11',
        'unit':'Deg.C',
        'description':'TSYS01 (CH5 0x77)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'tsys12',
        'unit':'Deg.C',
        'description':'TSYS01 (CH6 0x76)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'tsys13',
        'unit':'Deg.C',
        'description':'TSYS01 (CH6 0x77)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'tsys14',
        'unit':'Deg.C',
        'description':'TSYS01 (CH7 0x76)',
        'interval':60,
        'lb':10,
        'ub':40,
    },
    {
        'dbtag':'tsys15',
        'unit':'Deg.C',
        'description':'TSYS01 (CH7 0x77)',
        'interval':60,
        'lb':10,
        'ub':40,
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
