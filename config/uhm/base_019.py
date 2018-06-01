name = '(TBD)'
location = '(TBD)'
google_earth_link = '#'
note = 'bbb-based, eMMC'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDj3Evu2LYdn1UTDeJfnZWgim8ymO1Ke3Jx7Qq8OkX104bj0zwbFsizE3gcFrSjsfw8i1QWlLNaRbx9CRbJYCAFbkBGcXyidozdKTAJr+41WheCDqkIfOf75JLV5/o2zP3hIaEm+V4jQsJWST/i+oYFBbhDlynz5j4zJlTze5SRIRX5wIogKOERNzbYJkyS+8YdUIrmOlaDbB+6xvHDpWwf8yT1GmImg5ZeWAgukr1nv22lTC1NxA+unp2tY550AK/njLCg075nZVvvYC8ck9o22Np0EjRvHxxgKXO62z2svJeRjtMwDuuKgdRG6y/za7fZR8vnphK03b9lOyHU8NNX nuc@base-019'


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
