
id = 7
#tag = 'node-007'
name = 'Met. Station'
note = 'RPi Meteorological Station'

#arch = 'rpi'

log_dir = './log'
plot_dir = '../www'

plot_range = 24*14

xbee_port = '/dev/ttyAMA0'
xbee_baud = 115200

wait = 597

multi_sample = 5

conf = [
    {
        'dbtag':'Timestamp',
        'dbtype':'TIMESTAMP',
        'comtag':'ts',
        'unit':'',
        'description':'Time of sampling',
        'plot':False,
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
        'description':'Air Temperature (BME280)',
        'plot':True,
    },
    {
        'dbtag':'RH_280',
        'dbtype':'REAL',
        'comtag':'RH_280',
        'unit':'%',
        'description':'% Relative Humidity (BME280)',
        'plot':True,
    },
    {
        'dbtag':'UV_Si1145',
        'dbtype':'REAL',
        'comtag':'UV_Si1145',
        'unit':'(idx x100)',
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
    {
        'dbtag':'Wind_average',
        'dbtype':'REAL',
        'comtag':'Wind_avg',
        'unit':'m/s',
        'description':'Wind Speed (average)',
        'plot':True,
    },
    {
        'dbtag':'Wind_gust',
        'dbtype':'REAL',
        'comtag':'Wind_gust',
        'unit':'m/s',
        'description':'Wind Speed (gust)',
        'plot':True,
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

