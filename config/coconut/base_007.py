name = '(TBD)'
location = 'Coconut Island'
google_earth_link = '#'
note = 'bbb-based'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDFAQju9QREF9PtIG8gbexXUwzz59rqfcsQq7r5OHFUSxIeqdM1J1E1RUoZxsKOlUcIT1Rs8DvZZlodIycn7H7+50dpztl65xqQJapHIakyWr0x47fBn/fVmQOovgHEgorHokEPfkZqnE4z4XO2Yz6SL2dBDZwY8g48DC+8aCDCiacKTpGuVrCFbvc+f6UKx8qpASrddS6TTbRKaD0exeSwV8i5gvQ08a74M9F6HOxZqD83WFtFdXfXYr967NLov2LSwFfU6x/13nBhvcIm5MgIWPUk+zLMBxQpxMyQsBOWEEYAEQrIq5uV0mkB5KD5YnYxi78TU/YdHlUTDcCpPtO1 nuc@base-007'

#log2txt_output_path = '/var/uhcm/log'


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
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf,basename(__file__).split('.')[0].replace('_','-'))
