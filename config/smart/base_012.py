name = 'Palolo Base Station #1'
location = 'Chris\''
google_earth_link = 'https://goo.gl/maps/qXG7NQwCtrw'
note = 'Beaglebone Black, cape v0.4'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC5W2A0UY2OZPh6XZlBWrARwBX+Ta+jtWPov364Xu/VVMbo29E4NlVZ01vgVzy/9uGXFivVBZM/bdb/Tc398FO2GC8/96zAJ1AcMcqGEqd2ZIfwXlBxbDbazDb8slpJFZgpfPArq0erVjMJOcQp7JreCvfTBk7Y9KWiRAiqoSiXb9q1amWSIa92yl0shvlPeR42pkKkL2xnQBitDv/PjAn/ll2/OAJwC238xwVvLfKH8v63yLIOOAWWb2AXn3FJIRNxja+kMvG5jjbIyqo2Nc7oJni5by35L2VDK3J5F2PfEeQYls93oOfonnoEM5YslT9girR6KhTECt0+Nxf4lnCR nuc@base-012'


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
        'lb':12*60*60,
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
