
id = 19
name = 'SL personal'
note = 'UH MSB rm 228'

log_dir = './log'
plot_dir = '../www'

plot_range = 72

xbee_port = None
xbee_baud = None

wait = 30

conf = [
#    {
#        'dbtag':'How it is referenced in sampling.py and in the drivers',
#        'dbtype':'SQLite data type',
#        'comtag':'How it is identified in broadcast messages',
#        'unit':'physical unit of the readings',
#        'description':'as name',
#    },
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
        'description':'Barometric Pressure',
        'plot':True,
        'convf':lambda (x): x/1000.
    },
    {
        'dbtag':'T_180',
        'dbtype':'REAL',
        'comtag':None,
        'unit':'Deg.C',
        'description':'Temperature',
        'plot':True
    },
    {
        'dbtag':'Humidity_HTU21D',
        'dbtype':'REAL',
        'comtag':None,
        'unit':'%RH',
        'description':'Humidity',
        'plot':True
    },
    {
        'dbtag':'Temp_HTU21D',
        'dbtype':'REAL',
        'comtag':None,
        'unit':'Deg.C',
        'description':'Temperature',
        'plot':True
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
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

