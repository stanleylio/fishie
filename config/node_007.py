
id = 7
name = 'Met. Station'
note = 'RPi Meteorological Station'

log_dir = './log'
plot_dir = '../www'

xbee_port = '/dev/ttyAMA0'
xbee_baud = 115200

wait = 597

conf = [
    {
        'dbtag':'Timestamp',
        'dbtype':'TIMESTAMP',
        'comtag':'ts',
        'unit':'',
        'description':'Time of sampling',
    },
    {
        'dbtag':'P_180',
        'dbtype':'REAL',
        'comtag':'P_180',
        'unit':'Pa',
        'description':'Barometric Pressure',
        'plot':True,
        'convf':lambda (x): x/1000.
    },
    {
        'dbtag':'T_180',
        'dbtype':'REAL',
        'comtag':'T_180',
        'unit':'Deg.C',
        'description':'Casing Temperature',
        'plot':False
    },
    {
        'dbtag':'UV_Si1145',
        'dbtype':'REAL',
        'comtag':'UV_Si1145',
        'unit':'(idx x100)',
        'description':'UV Index x 100',
        'plot':True
    },
    {
        'dbtag':'IR_Si1145',
        'dbtype':'REAL',
        'comtag':'IR_Si1145',
        'unit':'lux',
        'description':'IR',
        'plot':True
    },
    {
        'dbtag':'Amb_Si1145',
        'dbtype':'REAL',
        'comtag':'Amb_Si1145',
        'unit':'lux',
        'description':'Ambient Light Intensity',
        'plot':True
    },
    {
        'dbtag':'Wind_average',
        'dbtype':'REAL',
        'comtag':'Wind_avg',
        'unit':'m/s',
        'description':'Wind Speed (average)',
        'plot':True
    },
    {
        'dbtag':'Wind_gust',
        'dbtype':'REAL',
        'comtag':'Wind_gust',
        'unit':'m/s',
        'description':'Wind Speed (gust)',
        'plot':True
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

