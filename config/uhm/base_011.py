name = '(TBD)'
location = '(TBD)'
google_earth_link = '#'
note = 'bbb-based'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDDC+ZgKHDCHMKOOGw8bcOxAC6Fib5OAtBVgPVNq42g58tTddu8XWLjYVwLlt8YZ6IAMUgnMdRrTLJJK+EEy50nXhSm4Zft2A3VU0YdxQJEp/LwyJJawOI0695oliSMVLCKcrGdZ25A7zR+jU2TdO5EELWqpiqdk6Nwfp3/zKrVDtm6MHhh13iH7kP2vTEsXg79yMLtuGuwAL8tPakVjik1/lC0FwMDOCffE8Rfdy4UCcTvqJwPhkL1cpN6z8UPbBePkJWCt2SKqitZYNk0bITh9ZwPHC78cP3IzcKbSJoFEQbKmmcDEvMMSwYsHmKhknPUKBO9Z4CMI3n0I0ljjWxr nuc@base-011'


XBEE_PORT = '/dev/ttyS1'
XBEE_BAUD = 115200
INTERVAL = 10
NGROUP = 1
XBEELOGDIR = '/var/uhcm/log'


conf = [
    {
        'dbtag':'system_clock',
        'description':'Device clock',
        'interval':60,
    },
    {
        'dbtag':'uptime_second',
        'description':'Uptime in seconds',
        'lb':5*60,
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
        for k,v in c.iteritems():
            print(k,':',v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf,basename(__file__).split('.')[0].replace('_','-'))
