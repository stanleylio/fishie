
id = 5
name = 'Lab Ref.'
note = 'MS5803 + BMP180 + MCP9808 temperature sensor comparison'

log_dir = './log'
plot_dir = '../www'

plot_range = 72

xbee_port = None
xbee_baud = None

wait = 30

conf = [
    {
        'dbtag':'Timestamp',
        'dbtype':'TIMESTAMP',
        'comtag':None,
        'unit':None,
        'description':'Time of sampling',
        'plot':False
    },
    {
        'dbtag':'P_180',
        'dbtype':'REAL',
        'comtag':None,
        'unit':'Pa',
        'description':'Barometric Pressure',
        'plot':True,
        'convf':lambda (x): x/1000.
    },
    {
        'dbtag':'T_180',
        'dbtype':'REAL',
        'comtag':None,
        'unit':'Deg.C',
        'description':'Temperature (BMP180)',
        'plot':True
    },
    {
        'dbtag':'P_5803',
        'dbtype':'REAL',
        'comtag':None,
        'unit':'kPa',
        'description':'Barometric Pressure',
        'plot':True
    },
    {
        'dbtag':'T_5803',
        'dbtype':'REAL',
        'comtag':None,
        'unit':'Deg.C',
        'description':'Temperature (MS5803-14BA)',
        'plot':True
    },
    {
        'dbtag':'Temp_MCP9808',
        'dbtype':'REAL',
        'comtag':None,
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

