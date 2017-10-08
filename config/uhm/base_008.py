name = '(TBD)'
location = '(TBD)'
google_earth_link = '#'
note = 'bbb-based'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDB5JLe9Jw/1N4coVncGZKbCcq3YAr+VoSkHGRxFBoRe+rxbyrsQ5CWdt0a0Vx/xavgs5YaDN6nHdzbAiMjfP5JRQdls2Vy6HYsJR2T6pAlG77Pv/qUJT5BRcQwZbWtgmuffB0f+gHbBqJ1pE0EhSu7p+J0Axp9JWkHTMn2eLpOtlyL9BcSul9yz8q0NV5TLM9klUGgzwqZ1I+J1pHTZU2pBuErIxhb0c4jDOkRtJZ5G91I2fZviUK3FM+fXmEG5Vwb0s6QRPY2wPUWCS621/BlFk1qkdb/aknOq6w7qupIhXAuGxcj8CqCzeA1lrUanZa3/d6CxlgUUy0FXmBMCGdV nuc@base-008'


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
