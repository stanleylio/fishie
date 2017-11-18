name = '(TBD)'
location = '(TBD)'
google_earth_link = '#'
note = 'bbb-based'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDbVe7lOZXvuRKbJCBUwg1B6LxwOF2G8Nmu80YnrALcVlr+dGNFlEgosErzc/zlB+LHkrrh+48XCT9llcI8Tib4Ja7q4u0S+XYDIPn2MHdM+waneBJLjGPChS4wx0sp7Q8hTHKwEw5PQAHBEEAHE34mBMIx6RQ8VpyPIRhKP+AkSyZoACnvzysrtuhEXvp0IaE/WTCk/vmQtiBp391iBsYZ2ZMwRRvjWKXoo2fXA4HigfvKBIUsBMTsf5yJvs8St3GTNIld1QVjABgNALAM2jGvZA/yk4J2Beh1ozFu9aC4vXNS7T4OqUNL1+zNLQsWfDi87N0hNZ+syWcP4e/3pXnd nuc@base-013'


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
        'lb':5*60,
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
        for k,v in c.iteritems():
            print(k,':',v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf,basename(__file__).split('.')[0].replace('_','-'))
