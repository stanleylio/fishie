name = '(TBD)'
location = '(TBD)'
google_earth_link = '#'
note = 'bbb-based, eMMC, v0.5.1 cape'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCl2+eDiksusC2xfGzp/5oLjbgfu7H6YLJDx/S2+0h9yMvM9cb1SwcHiM3lVd84PyviYrIC+Qb/KfNhehquYIOALaPtJFBLJLjGGaKAFgs1gpDzvmzi5rh2LjS7U4hYXjlP4D0UKwrlkgYyCTz7fLIwO+01Vss7Ae4KXtctGY/Knz1fLCS9r4C7luWWbMt9rD/P5ril/4O9VgBry4fFM+SHqp/ArYmqN/v7sY0M6V/44pD3Bnljsr7GyDWKQ85KVvrECoP7gIq+S3MEjmyBNPhl6rxY1vr9fyvVqeovIutrrKQRltgEgM312tHhTIf/YgxScBfjF3ZaQ5vNQ16F5Jf9 nuc@base-030'
tags = ['gateway', 'beaglebone']

conf = [
    {
        'dbtag':'ts',
        'description':'Device clock',
        'interval':60,
    },
    {
        'dbtag':'uptime_second',
        'description':'Uptime',
        'unit':'seconds',
        'lb':24*60*60,
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
