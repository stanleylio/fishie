name = 'East West Center Base Station'
location = 'East West Center'
google_earth_link = '#'
note = 'bbb-based, eMMC'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDRX98c1j9j217yMprVfIJr3S+Vp3u4ss1FP9d49o+ckNLYihBulKg7Tp92HLUqzVrTD0AqSb2AnBhX7kGXRnr9kxHfTxzK33IKmWE5pbOVV/VsKJrnawPwh61fSMWucGnfdefgcz/pbcvU01LpqR3jApZLuw95qjXUh8keZiUbhOJe5UwAbVeYTacflxNxUBiHhfJM5wf3cVgp46m9iRdfDWMq42QWxkPgj5zldAuEciH7xg80Pgm/75dPXKPejgwOv4Oru3MYTK3QBxwij1pJpucnysJigWI4EoYgDHNiXV9Rc6SgWIJHFE/Cf72mR2kmDNSYKS2GaqgGHXQ2cTZx nuc@base-015'


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
        'lb':60*60,
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
