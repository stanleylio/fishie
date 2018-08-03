name = 'Lyon Aboretum Base Station'
location = 'Lyon Aboretum'
google_earth_link = '#'
note = 'bbb-based, eMMC'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCsgWeQsM0Cn+Jo1+k+QkjiOARls4dPJF4xTa/tfCQMkHKz+KKVXcgyc7uGI7J5JlLsl7s7QsSsps3In1moruImrIoNCzeHydxM9cWyjpSTlashRJL7LMeOwigNz8lImF9apxjLmVuiGCToZ5q7SE5OWchj2WD+MtXAsGV1zMW5ET4lCplleb/uuBtMmlTPLebZcuWOqtZMoerPIiMMWCTdM0TgLjBut2sXOkYI1wecm1FDa9AtXIO+PlNn+lW4xwKeh8cHHmKYAJwlS4eqguOVS7oZniWkGjybG8XfMFeXjMwwh6/kmf+UG+dcVYOCcb0bN0Blmk7/WvHrc+9rzlGz nuc@base-021'


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
