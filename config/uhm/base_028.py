name = '(TBD)'
location = '(TBD)'
google_earth_link = '#'
note = 'bbb-based, eMMC, v0.5.1 cape'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC2krlPCaBIMWA6ek04z17vSjv8EDp/saKyUbCOAlcqskJWr19gHA++2vLVNBbGOksew4EXQzNmNS80Kq/YlIzqKzz5hGbbrTPGjp0WwkM1cWfhUJpJx8RHdxBeJVthqxg8RMWQB1ggkp1a1lSuo2eST8IWb9BM6PNfO1xeUnTPVA4f64Gb0f8eJvA6Gw4RR2xTT04PY1T7CVbwG/4Hy/oYhmK4bIs8M4W6H6pSOiO35ZFTu+uNkOFtij+EEz8YFGSZnBFfug45V4pyA/5D2u0Oa7KlLKAeSjLbbHX2VPWH6avq0x6lsgY7DQVdSEFpAdt7u260vYFKHTVRKN6gumI/ nuc@base-028'


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
