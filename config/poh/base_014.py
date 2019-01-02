# -*- coding: utf-8 -*-
name = 'Fūjin (2.4)'
location = 'Paepae o He\'eia, Kaneohe'
google_earth_link = 'https://goo.gl/maps/ECEBgo3UEp82'
note = 'XBee 900HP (cold standby) and 2.4GHz (anemometer controller for node-006). bbb-based, eMMC'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDUNeHyYu/A3z7pPmXgmR4f6AvCJDtcuSaF1Swf5h/szppdQBrSbXK0L6D6nA+CeGDHmM6OJK0F0JVeq+AHk77c+LZ98ngz0Nd49aagvRJIQJV25PKpyvugsp9MAwYZloiSQuNTObHZlDUhmhoea5cyuZ8xPVi2837X+5kt0ODZuSpqqtGoFiCVuhVfxo6axqsnnjUaMLFGSj0hmYnfKTMxVwl5hyKotarLAioZer2k+aDUm+I1xH3ez/XWo3uoaNx+l4UmDubk5hjRZ0//fl2kIcW6yKAoKl+VyDvBbaOavwQqbS2LIQreBaaOe5qvvMLhvItzboreL2BqJ7R9QpE3 nuc@base-014'
latitude = 21.431282
longitude = -157.806858


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
        for k, v in c.items():
            print(k, ':', v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf, basename(__file__).split('.')[0].replace('_', '-'))
