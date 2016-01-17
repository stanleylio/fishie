name = 'us1'
location = 'Makaha 2'
note = 'Ultrasonic Proof of Concept'

log_dir = './log'
plot_dir ='../www'

plot_range = 24*7

#wait = 400

#multi_sample = 7

conf = [
    {
        'dbtag':'ticker',
        'dbtype':'INT',
        'comtag':None,
        'unit':None,
        'description':'ticker',
        'plot':False,
        'min':0,
        'max':2**32 - 1,
    },
    {
        'dbtag':'d2w',
        'dbtype':'REAL',
        'comtag':None,
        'unit':'mm',
        'description':'Sensor to Water Surface',
        'plot':True,
        'min':300,
        'max':5000,
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

