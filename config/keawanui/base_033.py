name = 'Telemetry Gateway'
location = '(TBD)'
google_earth_link = '#'
note = 'bbb-based, eMMC, v0.5.1 cape'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1AjN8zgszaiAW6Fu4fpn1aawoU5T4XAsMFPv6zP2iAiOWFoUdOvM873n+WAyRhd0ckzsjn0pu3d4iovAPUpNRpE1NQter2u3tEY6ZCYLdRDdmweYtgmiqXS5AdhvfsyoerIK+DrFcSwDpsHy7R6UMxrRbmLOmbe4ggg4ve9LGy+z1Sx9PB0vPIphN8mSleYqcnLTEPMktPdqoOTe3n/IDTpYcYR0VL5J26TBDjRG63xmqhY3MGduvWpmyjnpstFSqHCtHvYAV1aTx5fVtcK7ke6xyo2Omihvl31AWQ3cje3a40IAS9DD42LbX7EDuvT79auJHvEfeXPInaJw6jHUJ nuc@base-033'
latitude = 21.05478
longitude = -156.85012


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
