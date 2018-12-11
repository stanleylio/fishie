name = '(TBD)'
location = '(TBD)'
google_earth_link = '#'
note = 'bbb-based, eMMC'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDw9aDDY50488G3wJ2HHAwGgNrVGssyKWvnHHxxHVc9kM6uqbWrZ007s8gwa8IoOLqtLrEedUDjpSI7oS9dy90UtyibYGn992Dc87Uzgcfd1gmOZyjwe2oF3Z4La6o6UXiAZIkhbbcEThCJmW3DwmnzjJnEbsZK/Pqh/JeMFDw1dWgQbhwaKnyco2T7FlpOkTzBGLJ0tkxpyxYxicuRUfxY6zKO+U8LjjjQFl9D34ypIksqIt/8gCkonX7xB/aN69Hssi8tshMhv6uHvX1i/oPuBII4yQYOOZr8/4kr55bR3ICKbIUduejluMbaWhOZ1TRixr/yGHbmJ6RiDh8/et4f nuc@base-017'


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
