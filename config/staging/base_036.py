name = '(TBD)'
location = '(TBD)'
google_earth_link = '#'
note = 'bbb-based, eMMC, v0.5.1 cape'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZrVwKIa8BGxeeMns5/E6X+CK1+6E8Z/BHRgL1vW0cgFiosGsbqRCV2oieNcI8hVZjoUQ8nE4EgWrWXOXzsIlFabGak/O7zDlgnJ/PiW6/lPPSlq1LnAoJyyuWylx1xCS4TPyyr78S7qbFE5Rdtrp2G+s6dKpt9Zlkkn9CoeHNKrW/S3a+KzzkzYh9W0+l6DxR72V+TSZCyo+IggVA7QrQk+5lxd41DfbaP7aExaUqcu6y+qOPDLEe3P9zeEHv+6ILl9n/p/tmT4cq8z7r2JS2ZVY3aKSie5pL/SaNUafaZoOmUZj0AhzuslV4412X6asPUTKJ1k+7Gb0M/ovEi+m1 nuc@base-036'
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
