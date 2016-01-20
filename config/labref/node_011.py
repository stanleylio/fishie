tag = 'node-011'
name = 'Waterbath'
note = 'MS5803 + BMP180 + MCP9808 in mineral oil'

log_dir = './log'
plot_dir = '../www'

plot_range = 24

xbee_port = '/dev/ttyO1'
xbee_baud = 115200

wait = 10

multi_sample = 3

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
        'description':'Water Pressure (BMP180)',
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
        'dbtag':'P_5803',
        'dbtype':'REAL',
        'comtag':'P_5803',
        'unit':'kPa',
        'description':'Water Pressure (MS5803-14BA)',
        'plot':True,
    },
    {
        'dbtag':'T_5803',
        'dbtype':'REAL',
        'comtag':'T_5803',
        'unit':'Deg.C',
        'description':'Temperature (MS5803-14BA)',
        'plot':True,
    },
    {
        'dbtag':'T_9808',
        'dbtype':'REAL',
        'comtag':'T_9808',
        'unit':'Deg.C',
        'description':'Temperature (MCP9808)',
        'plot':True,
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

