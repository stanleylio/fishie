name = 'Halau Ku Mana Base Station'
location = 'Halau Ku Mana School (Makiki)'
google_earth_link = '#'
note = 'RPi3 16GB. Replacing base-027.'
#public_key = ''
#latitude = 21.287222
#longitude = -157.717500

conf = [
    {
        'dbtag':'system_clock',
        'description':'Device clock',
        'interval':5*60,
    },
    {
        'dbtag':'uptime_second',
        'description':'Uptime in seconds',
        'lb':24*60*60,
        'interval':5*60,
    },
    {
        'dbtag':'usedMB',
        'unit':'MB',
        'description':'Used disk space',
        'interval':5*60,
    },
    {
        'dbtag':'freeMB',
        'unit':'MB',
        'description':'Remaining free disk space',
        'lb':800,
        'interval':5*60,
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
