
id = 2
name = 'Ocean Makaha 2'
note = 'Aanderaa 3835'

plot_dir = '../www'

plot_range = 72

conf = [
    {
        'dbtag':'Timestamp',
        'dbtype':'TIMESTAMP',
        'comtag':'ts',
        'unit':'',
        'description':'Time of sampling',
        'plot':False
    },
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

