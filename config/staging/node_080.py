name = 'MSB319 "Environmentals"'
location = '319 Marine Sciences Building, UH Manoa'
google_earth_link = '#'
note = ''
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCdptvYvxiefBlv9nQRSMzKSyYOJnZszmdu3cuw2SLKX9MXLPPGCpW5cGcXwrnqFy5JtBDkt/hiunEc9clt6+KsEMjSVyUmEjGaVwA4aCijJdrOkkFtHuiaGGPnm4KMGp6ynyQ49bbEWZcxY4D5qCsLPqN0/VL62FJEkGy/GHkRTy7Lq9I3EGyLBDSV4oIvfEdYDUEihSps77MdM33sqwa0xCNjolioZQsQWMNeeLcqOtBp/J6OwF9t+o5ZI2JdPUuT49kFXu0cyIIdbDfYcgtn/0OhI4TwMKVfqYrc5vttLwnGhkB13hdyT+yS86JI0muZdHZ4KMT4kGZbbGpHtzOz pi@node-080'


conf = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE NOT NULL',
        'description':'Time of sampling',
        'plot':True,
    },
    {
        'dbtag':'Ta',
        'unit':'Deg.C',
        'description':'CH0 TSYS01',
        'lb':-15,
        'ub':60,
    },
    {
        'dbtag':'light_count',
        'unit':'-',
        'description':'Ambient light (raw count, Si1145)',
        'lb':0,
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
    create_table(conf,basename(__file__).split('.')[0].replace('_', '-'))
