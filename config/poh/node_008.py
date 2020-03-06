name = 'Water Level (Kahoʻokele)'
location = 'Kahoʻokele (second mākāhā)'
note = 'Ultrasonic tide gauge (XBee). One measurement/second, one transmission/minute. 7\'4" to bottom. Deployed 20170522. Upgraded to hardware v5.3, firmware us14 on 20200128.'
latitude = 21.435435
longitude = -157.805250

# 20170522
#UPDATE uhcm.`node-008` SET VbattmV=VbattmV/1000.0;

conf = [
    {
        'dbtag':'d2w',
        'unit':'mm',
        'description':'Distance from sensor to water surface',
        'lb':301,
        'ub':4999,
        'interval':60,
    },
    {
        'dbtag':'std',
        'unit':'mm',
        'description':'Sample standard deviation',
        #'lb':?,
        #'ub':?,
        'interval':60,
    },
    {
        'dbtag':'Vb',
        'unit':'V',
        'description':'Battery voltage',
        'lb':3.7,
        'ub':4.2,
        'interval':60,
    },
    {
        'dbtag':'Vs',
        'unit':'V',
        'description':'Solar input voltage',
        'lb':0,
        'ub':7.0,
        'interval':60,
    },
    {
        'dbtag':'idx',
        'description':'Sample index',
        'lb':7*24*60,
        'interval':60,
    },
    {
        'dbtag':'sc',
        'description':'# of measurements within 3\u03c3',
        'lb':30,
        'ub':60,
        'interval':60,
    },
]


if '__main__' == __name__:
    for c in conf:
        print('- - -')
        for k, v in c.items():
            print(k, ':', v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf, basename(__file__).split('.')[0].replace('_', '-'))
