name = 'PoH Base Station (cold standby)'
location = 'Paepae o He\'ei, Kane\'ohe'
google_earth_link = 'https://goo.gl/maps/ECEBgo3UEp82'
note = 'bbb-based'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDDxQo/IVvzvYQJNif7XDD2UOwrQjbY6azURNA4K6QU7xMvDGJ7cohkib5sneCnLiL836VlT3AJ3Nj1cM/0UftJv1h8H836jfSvtTTdDhDwDg150c32VRq1AN8yoUyQMKsfKduuAAcdpRtTnVO3brNHn9o+pn/p36uepKF+kZUVKf75Bh9VqCldAzCbYx+jhWyRItpEKYqOftlcyyoM1GCIx+1R1143qR+onN1wSa2+N8KO6XFN0lFmaVAUC4guRffESMg6GS12GuJLT8iOYhDMFeMrjS9/Fn14zW7oRIungxHGYPYXsju1UmxaArtWfqj2wK/mioqZFktKUg9IT7Ex root@base-001'

#log2txt_output_path = '/var/uhcm/log'
#dbfile = '/var/uhcm/storage/sensor_data.db'
#subscribeto = ['127.0.0.1:9002']


conf = [
    {
        'dbtag':'system_clock',
        'description':'Device clock',
    },
    {
        'dbtag':'uptime_second',
        'description':'Uptime in seconds',
    },
    {
        'dbtag':'usedMB',
        'unit':'MB',
        'description':'Used disk space',
    },
    {
        'dbtag':'freeMB',
        'unit':'MB',
        'description':'Remaining free disk space',
        'lb':800,
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
