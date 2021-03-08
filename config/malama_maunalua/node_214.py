name = 'Alamuka Street BWS Rainfall'
location = 'Alamuka Street BWS, Wailupe'
note = 'Cellular rain gauge. Firmware uc0.3, hardware v0.4 (cellular).'
latitude = 21.291206
longitude = -157.753514

coreid = '37001e000947373432363837'

conf = [
    {
        'dbtag':'ts',
        'description':'Sample time (Electron clock)',
        'interval':60*60,
    },
    {
        'dbtag':'mm',
        'unit':'mm/hr',
        'description':'Hourly rain fall',
        'lb':0,
        'ub':10,
        'interval':60*60,
    },
    {
        'dbtag':'da',
        'unit':'mm/day',
        'description':'Daily rain fall',
        'lb':0,
        'ub':433,   # annual average, not likely to be higher than that...
        'interval':24*60*60,
    },
    {
        'dbtag':'Vb',
        'unit':'V',
        'description':'Battery voltage',
        'lb':3.7,
        'ub':5.5,
        'interval':60*60,
    },
    {
        'dbtag':'SoC',
        'unit':'%',
        'description':'State of Charge',
        'lb':30,    # more like a warning than a valid range check
        'ub':100,
        'interval':60*60,
    },
]


if '__main__' == __name__:
    for c in conf:
        print('- - -')
        for k, v in c.items():
            print(k, ':' ,v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf, basename(__file__).split('.')[0].replace('_', '-'))
