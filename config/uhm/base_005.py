name = 'Message Broker'
location = 'UHM'
google_earth_link = '#'
note = 'NUC6CAYS'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDkLNFZ/oJHnNrJ4nB0jke4NaeImloIGtQffGedarlDXZxGQ0F3id2v2MgKS3vLvlijTfbuP/V6v+ZQ3zDuwxIcg4okn6QKuHX+s1K9yd2rrVmler/aAAx3qz4rk0+ehSCxK41TQtQXPU+haHr4d+l9pmhqoZWJbgiPkXW64LRDEvWO5hwFVmKC1oJYfA5XzM4Z1e5SQcnwz3NvBcfsflfmuByJm2aPq6nDETs85hcJ4I+CwRVBkBfxDskw5jpQCqGUGAuvgSmTTtGPlkge+4Ov68fPtBu8pD/s0uJ7TXFhjuHtx0zTl6TeV6mQz3iMtcgqjCwLK4U8XxAViZNBbAiz nuc@base-005'


conf = [
    {
        'dbtag':'system_clock',
        'description':'Device clock',
        'interval':1*60,
    },
    {
        'dbtag':'uptime_second',
        'description':'Uptime in seconds',
        'interval':1*60,
        'lb':60*60,
    },
    {
        'dbtag':'usedMB',
        'unit':'MB',
        'description':'Used disk space',
        'interval':1*60,
    },
    {
        'dbtag':'freeMB',
        'unit':'MB',
        'description':'Remaining free disk space',
        'lb':10000,
        'interval':1*60,
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
