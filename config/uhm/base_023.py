name = 'WHOI'
location = 'WHOI'
google_earth_link = '#'
note = 'bbb-based, eMMC'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxtmw4j27NiKPsVqF/i5JblsN9BVsNFxZwqedSJqkbm5Zem7HSpEVRiLIAiX1vhj0Np8aw03IXGsSak4cvJUfmfpUhLwXZxCuNDEXOZdRfn3WLyP8Yb9GXraykV0DnUwdnMM3nqU11uK1MzsAEeyW06f5MtKSdZthvf07p+hanXgp9DKrzBmTWtetY4gezB8jcuR61fEDZAeJAExxEztIkx5iO8zpFUztam36FU24sM9a9PhHOb7OIKW3qzUpNhmJU6XMx3GBWhD0A6esgRFjj4kJcFt85vTtYw1/mwG19EaRdBaNKWPQOEciGFVp5Tz+YIkfbB8cApNonL1urnbLB nuc@base-023'


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
