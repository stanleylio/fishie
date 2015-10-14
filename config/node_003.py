
name = 'Ocean Break'
note = 'Aanderaa 4330F + FLNTU'

log_dir = './log'

xbee_port = '/dev/ttyO1'
xbee_baud = 115200

ms5803_bus = 1

optode_port = '/dev/ttyO4'
flntu_port = '/dev/ttyO2'

wait = 593

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
        'dbtag':'P_5803',
        'dbtype':'REAL',
        'comtag':'P_5803',
        'unit':'kPa',
        'description':'Water Pressure',
        'plot':True
    },
    {
        'dbtag':'T_5803',
        'dbtype':'REAL',
        'comtag':'T_5803',
        'unit':'Deg.C',
        'description':'Water Temperature (MS5803-14BA)',
        'plot':True
    },
    {
        'dbtag':'Chlorophyll_FLNTU',
        'dbtype':'REAL',
        'comtag':'chlorophyll',
        'unit':'-',
        'description':'Chlorophyll (raw count)',
        'plot':True
    },
    {
        'dbtag':'Turbidity_FLNTU',
        'dbtype':'REAL',
        'comtag':'turbidity',
        'unit':'-',
        'description':'Turbidity (raw)',
        'plot':True
    },
    {
        'dbtag':'Thermistor_FLNTU',
        'dbtype':'REAL',
        'comtag':'thermistor',
        'unit':'-',
        'description':'Thermistor (raw)',
        'plot':True
    },
    {
        'dbtag':'O2Concentration',
        'dbtype':'REAL',
        'comtag':'O2',
        'unit':'uM',
        'description':'Oxygen Concentration',
        'plot':True
    },
    {
        'dbtag':'AirSaturation',
        'dbtype':'REAL',
        'comtag':'Air',
        'unit':'%',
        'description':'Air Saturation',
        'plot':True
    },
    {
        'dbtag':'Temperature',
        'dbtype':'REAL',
        'comtag':'T_4330f',
        'unit':'Deg.C',
        'description':'Water Temperature (Aanderaa 4330F)',
        'plot':True
    },
    {
        'dbtag':'CalPhase',
        'dbtype':'REAL',
        'comtag':'CalPhase',
        'unit':'Deg',
        'description':'CalPhase',
        'plot':False
    },
    {
        'dbtag':'TCPhase',
        'dbtype':'REAL',
        'comtag':'TCPhase',
        'unit':'Deg',
        'description':'TCPhase',
        'plot':False
    },
    {
        'dbtag':'C1RPh',
        'dbtype':'REAL',
        'comtag':'C1RPh',
        'unit':'Deg',
        'description':'C1RPh',
        'plot':False
    },
    {
        'dbtag':'C2RPh',
        'dbtype':'REAL',
        'comtag':'C2RPh',
        'unit':'Deg',
        'description':'C2RPh',
        'plot':False
    },
    {
        'dbtag':'C1Amp',
        'dbtype':'REAL',
        'comtag':'C1Amp',
        'unit':'mV',
        'description':'C1Amp',
        'plot':False
    },
    {
        'dbtag':'C2Amp',
        'dbtype':'REAL',
        'comtag':'C2Amp',
        'unit':'mV',
        'description':'C2Amp',
        'plot':False
    },
    {
        'dbtag':'RawTemp',
        'dbtype':'REAL',
        'comtag':'RawTemp',
        'unit':'mV',
        'description':'RawTemp',
        'plot':False
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

