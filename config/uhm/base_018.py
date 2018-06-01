name = '(TBD)'
location = '(TBD)'
google_earth_link = '#'
note = 'bbb-based, eMMC'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC52uNUmH1qmgkdm554582VXQPLIxSOC36nQOhxtkcdht0h5lxcgp6XekqgPLwQQuM7/HuUoLs14dwqStuNKnXMHXMe+txC35lvT/AhmnpCGZAfUZZLKyreUlUcZs0zfNEp46eKhbzZ9rKyiObI2PPPUwnJPH5Zj13yTZpS97J7t+xiNmY7NFCcE72cBRi+KYSUwWWjxmqRBYlBKQfXSmKLiMZBFEuFpxSs5nEsQKM7rTvZfaW90ULWN8GZisgjr3w998qZCpZsPNUL+tOf8atQfL/y6uaV2s2aPStHV9rocOtwazhdgHFB0LQudjfXkxX/USPoQZ6yPVVH/EVwn2/9 nuc@base-018'


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
