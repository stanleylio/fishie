name = '(TBD)'
location = '(TBD)'
google_earth_link = '#'
note = 'bbb-based, eMMC'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC2IG89/hTmC2AJt2GT15nHsPZ/+1h6Pb4ezw795KOezuStN9Xnj10BAnSiwTJEaU+1B35VF23YSj3YBdbyQpOc1qh+YQK3ck2577LlNj6scYfMiIw8ZK50/a3nLpN0gWIANjzEnqyxsNhWEUIyztxJG8iLPRO5WVlpPZBpVQYAMIReBSXczFwjKzdOlLMhcrM3VUlp82dmI2gxY6qpINZTRDC+t9dsH0napfOvw6/M+TLl4/YAXzU8wPLd5d1EGA6clV+JMy1wE7eq3TPExm02Kx4eU8NEv+Mtu2AESnEgzLMEh07hoaHXr2V84LIuR1dKmuApeiNlid6YjfdsgR7F nuc@base-024'


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
        for k, v in c.items():
            print(k, ':', v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf, basename(__file__).split('.')[0].replace('_', '-'))
