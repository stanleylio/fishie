name = '(TBD)'
location = '(TBD)'
google_earth_link = '#'
note = 'bbb-based, eMMC, v0.5.1 cape'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC+BcAJBFbUQj9eU+W+P90kt87cXutCkpJ6vJOePQ66PibkZhVyo8MAiDQmUuwAXxe7WHxQACedOGqt0eV1OuGJrIDVLUaSqh23y1RoHOnfN07KtToygYkb8SrbzfkntiZuiC7EHtIk4HF8SX6WwY/0WN5OhiINsLNoA3qW0iAA2RqDJ7wJ5rWEwP/BXpv3TPdoaqzFHy83YZYuBzQJIKKkox7ihYH/JDiOolKwrOtMxGwREgaxZi3MUh/1KZHY7f8Qi/c3dzRo4GnmmPrDPszMMsEGS1Eua2hgtyd6g3IAwxvUo2SqJD0SOadVqtqeOHi8wyJWOcpqolhzo9boJRQL nuc@base-031'
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
