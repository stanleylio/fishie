name = '(TBD)'
location = '(TBD)'
google_earth_link = '#'
note = 'bbb-based, eMMC'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDhgQFlurXMUDbDIEyEZpPdw1htQ7gRhGrHcYkGYVrS42d1AaWE3SO017fPwkJvg0H670bfFcfjE/iR/w+cveRRuUyCq9OujOhzE98sggSPpyZFt4SEMgrh2CY3TGDWhG6/85ujeatSJ4wdbgc/C8wq9egwCxV0vrCDO58JA6iigsEcFfZmIzyUWHcTvLMHJ5BRky1PR0HGTbKtSMsZheQf58mN5sUaXTj46w0pBJ6gGvFpmx67zeT7SiZCld3NDNkNf2p6nFTiUfslw9tUpXcseLOZSGawWkDMBy5GKFCE/7anV/1SPkTZOvytCIQQCA7eVNzMO2xMuaMJCZS+7Sed nuc@base-025'
tags = ['gateway', 'beaglebone']

XBEE_PORT = '/dev/ttyS1'
XBEE_BAUD = 115200


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
