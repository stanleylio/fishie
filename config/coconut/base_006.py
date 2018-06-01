name = 'Boat house (rooftop omni)'
location = 'Boat house, Coconut Island'
google_earth_link = '#'
note = 'bbb-based'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDqAi8zlZtVqegzL5kRHsfdUxCTAo/vYNhG+Avk53NaiNALVawvKR9asNstHi+sF/gtYVe7K+Db90lRMEARc+8Y1PCIlGlcwQFFzEA9xgV/xrJmJTJZE1vHm3Uf9ol6fQscBZ01NeppeSJZJsUir2X2aHcqcpcTspX7kGIiQBDi6VjSX4EULdMmHGg5/ruWlkOXDUN+0Lp5y41X5LVcKtYHtrU9usYZR5H3o6ruplsvBnDuLBrEQF4tYIowt7cxDYA6abeCtZacMtGIHvYdwceMyYZZhMN1HtIrLjUDyfcMlXeCVkytOfF4lXMckXLxPSBYu4i4Jmv6XpNGYMffMURx nuc@base-006'

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
