name = '(TBD)'
location = '(TBD)'
google_earth_link = '#'
note = 'bbb-based, eMMC, v0.5.1 cape'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDEDEkaSbt9dUzGB9m6f1MNj3Kopt3uMQSlnX5mzpgki4sdGLjOr7idKnLHFj9oBFfkN/7bHABbTPL78DAGzZlJ1yTVLihU4pdQ1+JrhnToxHn36SLJBSntAKXpcCzTSZ0O7sUNjT5VkfOpcs37CgHc4zHXIQhY2SRUY7Wl2epxOWrW1l1JGhMPrll7HBsnl+mOC96IALZVGm4YH1YXbF4IJ6WG3g0wJYf2Tyni0HnqAv3nVtlzNtSTUYzDCCQ6Dru33ifFCdwMn5jUyK9SD0/qeE0rz1vtbI2KIz/9hXWX2cjFJhgi1hQqDAeHHf0mC2ONX4Nn3Q+p2oKuzmY+Fl7Z nuc@base-035'


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
