
id = 1
#tag = 'node-001'   # slated to repalce the numerical node ID
name = 'Triple Makaha'
note = 'Aanderaa 3835'

plot_dir = '../www'

plot_range = 168

conf = [
    {
        'dbtag':'Oxygen',
        'dbtype':'REAL',
        'comtag':'O2',
        'unit':'uM',
        'description':'O2 Concentration',
        'plot':True
    },
    {
        'dbtag':'Saturation',
        'dbtype':'REAL',
        'comtag':'Air',
        'unit':'%',
        'description':'Air Saturation',
        'plot':True
    },
    {
        'dbtag':'Temperature',
        'dbtype':'REAL',
        'comtag':'T',
        'unit':'Deg.C',
        'description':'Water Temperature',
        'plot':True
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

