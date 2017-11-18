# -*- coding: utf-8 -*-
# us2
name = 'Hīhīmanu Water Level'
location = 'Hīhīmanu (first mākāhā)'
note = 'Ultrasonic tide gauge (us2)'


conf = [
    {
        'dbtag':'ticker',
        'dbtype':'INTEGER',
        'description':'Broadcast sequence number',
        'lb':0,
        'interval':400,
    },
    {
        'dbtag':'d2w',
        'dbtype':'REAL',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'lb':301,
        'ub':4999,
        'interval':400,
    },
    {
        'dbtag':'VbattmV',
        'dbtype':'INTEGER',
        'unit':'mV',
        'description':'Battery voltage (Vcc)',
        'lb':2400,
        'interval':400,
    },
]


if '__main__' == __name__:
    for c in conf:
        print('- - -')
        for k,v in c.iteritems():
            print(k,':',v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf,basename(__file__).split('.')[0].replace('_','-'))
