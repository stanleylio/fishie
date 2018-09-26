name = 'Mokauea Island Telemetry Relay'
location = 'Marine Education Training Center, HCC'
google_earth_link = '#'
note = 'bbb-based, eMMC'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDt/+/JZXnpt63qjeQRBCxV0gR6OTKqLYI6yyQUwbC7HQjA6CRtJ15r8zRuBmf2+ytt775syet1ssvTtjUFWwRVb6sqkPAg3sSQDVuVqdXSjCAUOCuzmf3x8lFxMzPGYjlq8fLt5GrinqMnhswv2Xz0mVd1eAheKD2QhWVzXxVdmdMHoc+A2KU7Z/Hjb7RC4SjoCfQk3eUvAVVsfMmia/FRiPxuqh4pGSJ9bbA7CQ6e9BL1EHkRrihgySu/5QI1W7TI6Qy2pBcugTpaG72nIlC5xC6mV6e58BNB0NiCZSBd+ElHmEhYQNL95VFCsQQs5XmRJ0nW9sscUyKzeM3Qgg45 nuc@base-022'


XBEE_PORT = '/dev/ttyS1'
XBEE_BAUD = 115200


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
