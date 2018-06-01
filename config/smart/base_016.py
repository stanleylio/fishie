name = 'Kānewai Base Station'
location = 'Kānewai'
google_earth_link = '#'
note = 'bbb-based, eMMC'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDwzpUztLLkhhF6ItntZTzgHvFNwtFL5zLuda/vruHcxnBAsS7KtDHR3ugtV5I8BmErDzS/DuYhEdkfvV10dqSKgEuKhHY372thzFYiW+9pKSBlxOLLj0c6b+njIrTENF/h8ghBHRn+K3eeXeUTTzZNrI/DlSTW4Kt7cvpQUD8tN9TdVOUdaYNrsr7DJIHgNIlo8nJ4Thxr1Al/FFjR3BNXRttAg0ROS8ytj46ujYOzEbk0a2L2LFNHX1tpHOQvA4PIjUksfmbh8wgC1KUUCPpCcsXcVEc2ee6vGWt3lXves8aLVxKIAsc4QBdbT67rIwSaFYfZDlDGcVct0saYk04b nuc@base-016'


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
        for k,v in c.iteritems():
            print(k,':',v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf,basename(__file__).split('.')[0].replace('_','-'))
