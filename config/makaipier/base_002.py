name = 'Makai Pier Base Station'
location = 'Makai Research Pier, Waimanalo, Oahu, Hawaii'
google_earth_link = 'https://goo.gl/maps/BThU5mQNcPn'
note = 'Beaglebone-in-a-Box (base-002)'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAnKsvPuLQ0b3LtS8YJ28FEEZyRfY5GbpQSbbWjqojBn2AhbXIBo6D7D2c2j2OOcRkh7+3dyX7nyCjn0Yojb21sZxrW26jmT+7Zbi4N88Hexqd20RIjKeECA5ahUq8Kk+vG9qZvozXUR4RLyopn8bQ5240WlenNUxD2am81SxJzfJsMWeQniff9uiCnab+EZrbTn/CxgQex9cvgrbsRtoEUQwpO9bnXJpPhjGZdF/1PfDmDJvsd0NUa/SU8xTCh7ASLfQIopvxq9GuRN2GyfnW9HO4r0YBuBKt4oixJJRVlRF6RLv0LHTjQVEuRmmPwTEsGkwywGPn/9asbS4oBPF5 root@base-002'


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
        'lb':500,
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
