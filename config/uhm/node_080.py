name = 'Dell E3 Exhaust Temperature'
location = 'MSB228, UHM'
google_earth_link = '#'
note = ''
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCdptvYvxiefBlv9nQRSMzKSyYOJnZszmdu3cuw2SLKX9MXLPPGCpW5cGcXwrnqFy5JtBDkt/hiunEc9clt6+KsEMjSVyUmEjGaVwA4aCijJdrOkkFtHuiaGGPnm4KMGp6ynyQ49bbEWZcxY4D5qCsLPqN0/VL62FJEkGy/GHkRTy7Lq9I3EGyLBDSV4oIvfEdYDUEihSps77MdM33sqwa0xCNjolioZQsQWMNeeLcqOtBp/J6OwF9t+o5ZI2JdPUuT49kFXu0cyIIdbDfYcgtn/0OhI4TwMKVfqYrc5vttLwnGhkB13hdyT+yS86JI0muZdHZ4KMT4kGZbbGpHtzOz pi@node-080'


#subscribeto = ['127.0.0.1:9002']
#log2txt_output_path = '/var/uhcm/log'


conf = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE NOT NULL',
        'description':'Time of sampling',
        'plot':False,
    },
    {
        'dbtag':'tsys0',
        'dbtype':'DOUBLE',
        'unit':'Deg.C',
        'description':'CH0 TSYS01',
        'lb':-15,
        'ub':60,
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
