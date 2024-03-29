name = 'Backup Database and Broker'
location = '(TBD)'
google_earth_link = '#'
note = 'NUC5CPYH'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCuAIuai8QXOsi2KTzJrNVBFXvWMvqUQ5QKGYVzo7/Qr6gxj8xZZCcdukFFkTrCvHEsl7J0gHNsdwakTs+jVw8F7km4MPozGAMXoDEV/wWcXIxoaObUjRYsoUjArWrjsw3HlMbM+juKCYOPQsk8nYLpqv3BQ0Vc6p36OVDmIUfqNpwYxb6lpjgGo6j3npg+zgc8wfa5OyOBSEB5nkYN9k2WvJlKRVtDgvb4LA1lvTthPwb8z8jwFI2AV/Dr5SB1+miTQKbLmav/R6Uzpgxlc8mAMg9xz4NVQYm5t/uuCfigSG9S7oYg2FewNElO3zvykuTYHlVlFK6m55LaTE0gLSPr nuc@base-004'

log2txt_output_path = '/var/uhcm/log'

#subscribeto = ['127.0.0.1:9002']
#zmq2http_url = 'https://grogdata.soest.hawaii.edu/api/5/uhcm'
#dbfile = '/var/uhcm/storage/sensor_data.db'


conf = [
    {
        'dbtag':'system_clock',
        'description':'Device clock',
        'interval':60,
    },
    {
        'dbtag':'uptime_second',
        'description':'Uptime in seconds',
        'interval':60,
        'lb':60*60,
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
        'interval':60,
        'lb':10000,
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
