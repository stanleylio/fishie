
id = 6
#tag = 'node-006'
name = 'EZO demo'
note = 'EZO...'

log_dir = './log'
plot_dir = '../www'

plot_range = 1

xbee_port = '/dev/ttyO1'
xbee_baud = 115200

wait = 0

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
        'dbtag':'ec',
        'dbtype':'REAL',
        'comtag':'ec',
        'unit':'uS',
        'description':'Conductivity',
        'plot':True
    },
    {
        'dbtag':'sal',
        'dbtype':'REAL',
        'comtag':'sal',
        'unit':'',
        'description':'Salinity',
        'plot':True
    },
    {
        'dbtag':'do',
        'dbtype':'REAL',
        'comtag':'do',
        'unit':'uM',
        'description':'Dissolved Oxygen',
        'plot':True
    },
    {
        'dbtag':'ph',
        'dbtype':'REAL',
        'comtag':'ph',
        'unit':'',
        'description':'pH',
        'plot':True
    },
    {
        'dbtag':'orp',
        'dbtype':'REAL',
        'comtag':'orp',
        'unit':'',
        'description':'Oxygen Reduction Potential',
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

