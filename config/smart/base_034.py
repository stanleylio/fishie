name = 'St. Louis School Gateway'
location = 'St. Louis School'
google_earth_link = '#'
note = 'bbb-based, eMMC, v0.5.1 cape'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDLJDaYmc+X8Adi6k+ySq8U8DxWp+uVNh/xKzDvyQMKQ/bSY2lM1raf+mUH88GanDKjU1HLrRWFkCFkAE2awucv52hK/BkDp+mPD5Rr0/00UYXQo/fJbo4v4WZfrO29e4Lvl6uTP5bXv5ibn9WA4zvTcnDyV5A/istoBC1fJEPYkRAWrptopYHJV2tHGe1qDXpDFr0AA57L7qiK9OvdvrExBo2Um3QrHYDrjO+PNeCZnY+3Ls5pT6NLv6+KNTq6ROS9NCDlhRhe0TMoBGJvS2Q4dToD4ed52r3o86hwSAtpGZpUqesKTPjqzzaweFq9lQyhLC3KseB9AmzqXTOX4f37 nuc@base-034'
latitude = 21.28797
longitude = 157.80666


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
