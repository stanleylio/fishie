name = 'PoH Base Station'
location = 'Paepae o He\'eia, Oahu, Hawaii'
google_earth_link = 'https://goo.gl/maps/ECEBgo3UEp82'
note = 'NUC5CPYH (base-003)'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCzWObx6WFAfxuC3uDzAs2Ifq/rnxkhHQit6qKQ7RnuDfE3y8NmpyuZlWuYGHplNDCzXSILBXZTTA/rsrZuPfr6iKp8jNE6LRwf5dSx2jrY2pf7kXW+rWfSGFaAhHU73E/iZaOFBVccQmQFPsZPFN7n+sGMEDNI3bzMVsdZ+uKdv5FQArOSZISRpIol7HWJQ2mRdaZhqE7XgNrCugeihCunVusVlLnFaNomJnCy9yAxE3k5FmyUwGtYgDSY+zNEwCfXJasUfkxg4KIZrizZegr9o2bKi/5jCifMUpaeTvq4bfShe6AymZ2ADHPpyT6XWPxu4sHuOYVQ2GDIyeUl8CQX nuc@celeron-nuc'

#subscribeto = ['127.0.0.1:9002']
#sampling_serial_ports = [('/dev/ttyUSB0',115200),('/dev/ttyUSB1',115200)]
#log2txt_output_path = '/var/uhcm/log'
#dbfile = '/var/uhcm/storage/sensor_data.db'


conf = [
    {
        'dbtag':'system_clock',
        'description':'Device clock',
    },
    {
        'dbtag':'uptime_second',
        'description':'Uptime in seconds',
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf,basename(__file__).split('.')[0].replace('_','-'))
