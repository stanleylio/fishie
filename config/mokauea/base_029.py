name = 'Mokauea Island Telemetry Gateway'
location = 'Mokauea Island (21.308333, -157.891944)'
google_earth_link = '#'
note = 'bbb-based, eMMC, v0.5.1 cape'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDSSpJWf2tzhTsqRJLDXKZ/3MknFl1C9LMUHxCeWi8TvyRBFglSbFr1axO0B9eQenHCg6EXjehIMLURIuM84Oz9Zs+jJyiEp2aMrttlicc6wF7vtsZf0ORYS/Snq4i6KuYE8R09OFxByeBM3NZkz8YXOrxxaIwnawpJDFCgtJkln89j/5IbGrKPviGlfehyVqehT1aIwRiMfCD9YJNFBmb3xln0X2B0ZZfCkANSILA3xe9pcCw7kerqSeFNghC3gQgZ5YwkMJSvqZxowtl8Bsd20ckJaacrUr0sPLP+jxgzzDkwxW481AkUzRdFYT2nIfSExAaf2jGtc+wvMejIHh+L nuc@base-029'


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
