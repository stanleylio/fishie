# -*- coding: utf-8 -*-
name = 'Low-power Multi-sensor Node'
location = 'Kahoʻokele (Mākāhā 2)'
note = 'First low power CTD/O2/Turbidity/Chlorophyll node'


conf = [
    {
        'dbtag':'Timestamp',
        'dbtype':'DOUBLE NOT NULL',
        'description':'Time of sampling',
        'plot':False,
    },
    {
        'dbtag':'P_5803',
        'unit':'kPa',
        'description':'Water Pressure',
        'lb':90,
        'ub':180,
    },
    {
        'dbtag':'T_5803',
        'unit':'Deg.C',
        'description':'Water Temperature (MS5803-14BA)',
        'lb':0,
        'ub':50,
    },
    {
        'dbtag':'EC_4319A',
        'description':'Electrical Conductivity (Aanderaa 4319A)',
    },
    {
        'dbtag':'T_4319A',
        'unit':'Deg.C',
        'description':'Water Temperature (Aanderaa 4319A)',
    },
    {
        'dbtag':'Chlorophyll_FLNTUS',
        'description':'Chlorophyll (raw count)',
    },
    {
        'dbtag':'Turbidity_FLNTUS',
        'description':'Turbidity (raw)',
    },
    {
        'dbtag':'O2_optode',
        'unit':'uM',
        'description':'Oxygen Concentration',
        'lb':0,
        'ub':500,
    },
    {
        'dbtag':'Air_optode',
        'unit':'%',
        'description':'Air Saturation',
        'lb':0,
        'ub':150,
    },
    {
        'dbtag':'T_optode',
        'unit':'Deg.C',
        'description':'Water Temperature (Aanderaa 4330F)',
        'lb':0,
        'ub':50,
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

    import sys
    sys.path.append('../..')
    from storage.storage2 import create_table
    conf.insert(0,{'dbtag':'ReceptionTime','dbtype':'DOUBLE NOT NULL'})
    create_table(conf,__file__.split('.')[0].replace('_','-'))
    
