#tag = 'node-019'
name = 'SL personal'
location = 'MSB 228'
note = 'LA Beaglebone + eBay sensors'

#log_dir = './log'
#plot_dir = '../www'

#plot_range = 24*7


INTERVAL = 5*60
NGROUP = 7

LOGDIR = '/var/uhcm/log'
#data_source = '/home/nuc/data/node-019/storage/sensor_data.db'
DBPATH = '/var/uhcm/storage/sensor_data.db'


#wait = 60

#multi_sample = 7

conf = [
    {
        'dbtag':'Timestamp',
        'dbtype':'TIMESTAMP',
        'comtag':'ts',
        'unit':None,
        'description':'Time of sampling',
        'plot':False,
    },
    {
        'dbtag':'P_180',
        'dbtype':'REAL',
        'comtag':'P_180',
        'unit':'Pa',
        'description':'Barometric Pressure (BMP180)',
        'plot':True,
    },
    {
        'dbtag':'T_180',
        'dbtype':'REAL',
        'comtag':'T_180',
        'unit':'Deg.C',
        'description':'Temperature (BMP180)',
        'plot':True,
    },
    {
        'dbtag':'RH_HTU21D',
        'dbtype':'REAL',
        'comtag':'RH_HTU21D',
        'unit':'%RH',
        'description':'Humidity (HTU21D)',
        'plot':True,
    },
    {
        'dbtag':'T_HTU21D',
        'dbtype':'REAL',
        'comtag':'T_HTU21D',
        'unit':'Deg.C',
        'description':'Temperature (HTU21D)',
        'plot':True,
    },
    {
        'dbtag':'UV_Si1145',
        'dbtype':'REAL',
        'comtag':'UV_Si1145',
        'unit':'(100x index)',
        'description':'UV Index x 100',
        'plot':True,
    },
    {
        'dbtag':'IR_Si1145',
        'dbtype':'REAL',
        'comtag':'IR_Si1145',
        'unit':'lux',
        'description':'IR',
        'plot':True,
    },
    {
        'dbtag':'Amb_Si1145',
        'dbtype':'REAL',
        'comtag':'Amb_Si1145',
        'unit':'lux',
        'description':'Ambient Light Intensity',
        'plot':True,
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

