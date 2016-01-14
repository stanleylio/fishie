
id = 8
#tag = 'node-008'
name = 'Ultrasonic Proof of Concept'
note = 'Distance to Water Surface'

log_dir = './log'
plot_dir ='../www'

plot_range = 24*7

#wait = 400

#multi_sample = 5

conf = [
    {
        'dbtag':'d2w',
        'dbtype':'REAL',
        'comtag':None,
        'unit':'mm',
        'description':'Distance to Water',
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

