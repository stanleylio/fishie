name = 'Tempbath Station'
location = 'MSB301, UHM'
google_earth_link = '#'
note = 'Wifi bone; cape v0.2; base-007'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC9r/ROdI2KoSGWsizk8fhcUWONAMpAQsxJF8v8qyhZBVBGYT54bHWeTogcSl+cKmocqEvEY9HoL5APmqCGMy7k7MAKNIuN2AoEJm6bBia50vdtIK1LpMalHQ/dwaghsTU5a0nbC6eUiMUzTChiUSpzO3vH7Gj4hYITUwbpOlWTW5NVE7iRRSb/CiXu22m1hMuR5cyFzUzap5cQDmWULFCNyq4sSI6TZJru41kgrgs+x1UkdwOZmXDAgGmxqv8Pqj9WRWvd2KZNa6bXR+D7PfqYO6d+IvuS1eu2mD3WT6mqPIx2Om3He5m/GjVPTWlNkHExSAOpbZfMOsn9lrIeKtGX nuc@base-007'

XBEE_PORT = '/dev/ttyO2'
XBEE_BAUD = 115200
INTERVAL = 5
NGROUP = 1
XBEELOGDIR = '/var/uhcm/log'

subscribeto = ['127.0.0.1:9002']
log2txt_output_path = '/var/uhcm/log'


conf = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE NOT NULL',
        'description':'Time of sampling',
        'plot':False,
    },
    {
        'dbtag':'tsys0',
        'dbtype':'DOUBLE',
        'unit':'Deg.C',
        'description':'CH0 TSYS01',
        'lb':-15,
        'ub':60,
    },
    {
        'dbtag':'si0',
        'dbtype':'DOUBLE',
        'unit':'Deg.C',
        'description':'CH0 Si7051',
        'lb':-15,
        'ub':60,
    },
    {
        'dbtag':'tsys1',
        'dbtype':'DOUBLE',
        'unit':'Deg.C',
        'description':'CH1 TSYS01',
        'lb':-15,
        'ub':60,
    },
    {
        'dbtag':'si1',
        'dbtype':'DOUBLE',
        'unit':'Deg.C',
        'description':'CH1 Si7051',
        'lb':-15,
        'ub':60,
    },
    {
        'dbtag':'tsys2',
        'dbtype':'DOUBLE',
        'unit':'Deg.C',
        'description':'CH2 TSYS01',
        'lb':-15,
        'ub':60,
    },
    {
        'dbtag':'si2',
        'dbtype':'DOUBLE',
        'unit':'Deg.C',
        'description':'CH2 Si7051',
        'lb':-15,
        'ub':60,
    },
    {
        'dbtag':'tsys3',
        'dbtype':'DOUBLE',
        'unit':'Deg.C',
        'description':'CH3 TSYS01',
        'lb':-15,
        'ub':60,
    },
    {
        'dbtag':'si3',
        'dbtype':'DOUBLE',
        'unit':'Deg.C',
        'description':'CH3 Si7051',
        'lb':-15,
        'ub':60,
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table

    conf.insert(0,{'dbtag':'ReceptionTime','dbtype':'DOUBLE NOT NULL'})
    create_table(conf,basename(__file__).split('.')[0].replace('_','-'))
