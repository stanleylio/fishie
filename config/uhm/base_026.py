name = '(TBD)'
location = '(TBD)'
google_earth_link = '#'
note = 'pi-based'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDiq0j+vKL7sqqsxKdzVdNKG9jQPQGzFdrM9RRUsN1OoaAMzLcm8Q9+LKQ0Sc8INx1bC164pUe9CjJ+MlGj5WJoZpXioXH6xelSVL8FXvCtuOaIfAK5YBsRgw+B6UyrwUMl4e8KCoC8uTCuB3BXlioIkEAnrKpiBXO2DAFrV0X5+7wR7xiN8uReuYnBZ/zYbV/aIVuSidff/EcmnIl7cECnHU9mhLiKyyXTN7fiXgp/Q3/mFcZn0eBNOIre237zbwcg3IIjTiN/pQ2z0pBkTFTjaEZid8oHO6CMzY3wjOy0KCSqQOkgiAqnwbaTWSCxQcDJLMOhsRlHLNZ1I+D1ggFX nuc@base-026'


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
