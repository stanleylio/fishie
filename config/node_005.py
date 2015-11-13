
id = 5
#tag = 'node-005'
name = 'Lab Ref.'
note = 'MS5803 + BMP180 + MCP9808 + BME280 + HTU21D temperature sensor comparison'

log_dir = './log'
plot_dir = '../www'

plot_range = 24*14

xbee_port = '/dev/ttyO1'
xbee_baud = 115200

wait = 60

multi_sample = 7

conf = [
    {
        'dbtag':'Timestamp',
        'dbtype':'TIMESTAMP',
        'comtag':'ts',
        'unit':None,
        'description':'Time of sampling',
        'plot':False
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
        'plot':True
    },
    {
        'dbtag':'P_280',
        'dbtype':'REAL',
        'comtag':'P_280',
        'unit':'kPa',
        'description':'Barometric Pressure (BME280)',
        'plot':True,
    },
    {
        'dbtag':'T_280',
        'dbtype':'REAL',
        'comtag':'T_280',
        'unit':'Deg.C',
        'description':'Temperature (BME280)',
        'plot':True
    },
    {
        'dbtag':'RH_280',
        'dbtype':'REAL',
        'comtag':'RH_280',
        'unit':'%RH',
        'description':'Humidity (BME280)',
        'plot':True
    },
    {
        'dbtag':'RH_HTU21D',
        'dbtype':'REAL',
        'comtag':'RH_HTU21D',
        'unit':'%RH',
        'description':'Humidity (HTU21D)',
        'plot':True
    },
    {
        'dbtag':'T_HTU21D',
        'dbtype':'REAL',
        'comtag':'T_HTU21D',
        'unit':'Deg.C',
        'description':'Temperature (HTU21D)',
        'plot':True
    },
    {
        'dbtag':'P_5803',
        'dbtype':'REAL',
        'comtag':'P_5803',
        'unit':'kPa',
        'description':'Barometric Pressure (MS5803-14BA)',
        'plot':True
    },
    {
        'dbtag':'T_5803',
        'dbtype':'REAL',
        'comtag':'T_5803',
        'unit':'Deg.C',
        'description':'Temperature (MS5803-14BA)',
        'plot':True
    },
    {
        'dbtag':'T_9808',
        'dbtype':'REAL',
        'comtag':'T_9808',
        'unit':'Deg.C',
        'description':'Temperature (MCP9808)',
        'plot':True
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

