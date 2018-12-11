name = '(TBD)'
location = '(TBD)'
google_earth_link = '#'
note = 'bbb-based, eMMC, v0.5.1 cape'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3Y+1uSKeSuS5sfX4YTCDncjfOpbOFik3jcweS3lkNe48LRFu+1JmzZXGEFW9dFY0c2ozHRwgndAwncylQ9LyeSEHBlD/Q3iUUPsmNTjC0X8bqCPI/TbPN/qPkntYfXHS+GVU2VEDlYytD7QGxKcp4ADDK4mBErj0nD9TGHPGICTUtEwB6tb41gMYF9uYv+Y6hG2uiquYux4fl1UhUnIpMaMhqlclBE9P0VU5NT3UnvNFxLG7u/SvBsNF8Ya/7c6ymd1HgbSHFGH/YsTD6G9Y/wpzmfxGCJduixdfXdH7dANseQBjhsssumXRu1HApqYzaFsiwGYQUfRALbijCX/8h nuc@base-032'


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
