#name = 'Halau Ku Mana Base Station'
#location = 'Halau Ku Mana School (Makiki)'
name = '(TBD)'
location = '(TBD)'
google_earth_link = '#'
note = 'bbb-based, eMMC, v0.5.1 cape. Replacing base-007.'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDHucGXfEnuws7Y76/FLgegW0e0LZdz8OdbrRBjkZEllfFvhtVxuuEUaA/ocL1WO8uDBAuyxpyDRvsg1zIoHDqqGq4SXSWCsI+uegEZlRzyPk/683VdikFyFJ1pSP8LBb/j55oGoIAmkjsQyT5r2inbIlM7SAqeI98jukYiZWoe+LD1SmOT+6ZoOlKUD1fPVDj0ifQ9S6WGKOmd5SlvAdHo0rs/J67w5fBJ7M7e+Sq+WOgOI2X/Foz3nj0KlG5Ky8rJ1Ppd9TAY1lfg+BiFYKJVfeL5xT49K/ZSG8/aXptBEj+yqwTn4k+4/I16CHlcYD6u65j46DhiVGVlIacOwX/7 nuc@base-027'
tags = ['gateway', 'beaglebone']

conf = [
    {
        'dbtag':'system_clock',
        'description':'Device clock',
        'interval':60,
    },
    {
        'dbtag':'uptime_second',
        'description':'Uptime in seconds',
        'lb':24*60*60,
        'interval':60,
    },
    {
        'dbtag':'usedMB',
        'unit':'MB',
        'description':'Used disk space',
        'interval':60,
    },
    {
        'dbtag':'freeMB',
        'unit':'MB',
        'description':'Remaining free disk space',
        'lb':800,
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
