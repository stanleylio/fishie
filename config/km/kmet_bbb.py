subscribeto = ['localhost:9002','192.168.1.167:9002']
private_key_file = '/root/.ssh/id_rsa'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDN3PGFM+Ti+v/3CecZd5ls6G8OgVw4yFTtaFjVIDHmL51bC5ibKzelL7ZM+WU5WrRyeJmUNuK8IftFuQpQfJnGEhF7vpBpKhHQUK5SEMmcxPczKi0RWEelefE/IN1GlrnkDqQV7YMfasKSuhWq4OjgNsO0CxF18gatagPmOIiXZjXh7gMUF52d4faeU3oh5IxhO1+h+cx8jxRzovrNxicsbbYVOPc0pLw6WUIpDUsh7RDxxgiE3FCRdkxCYl8QJAhvtaXxbq/OnE8qRkTbi8aZ16D88qsaSjd31U2UmPqFJOuaYt8VDGYXw7rA9zmzufBxB2rfMRb2hSeb/qSv43c7 root@beaglebone'
data_dir = '/var/kmetlog/data'
log_dir = '/var/kmetlog/log'
service_discovery_port = 9005
realtime_port = 9007


DAQ_HV_PORT = ('/dev/ttyUSB0',1)    # serial port to DAQ, and its RS485 ID
DAQ_LV_PORT = ('/dev/ttyUSB1',2)
DAQ_F_PORT = ('/dev/ttyUSB2',3)

# or record all channels and map later?
# well the mapping has to live somewhere anyway. so here.
DAQ_CHANNEL_MAP = {'PIR_mV':('LV',2),
                   'PIR_case_V':('HV',6),
                   'PIR_dome_V':('HV',7),
                   'PSP_mV':('LV',5),
                   'PAR_V':('HV',5),
                   'BucketRain_accumulation_mm':('HV',0),
                   'Rotronics_T':('HV',1),
                   'Rotronics_RH':('HV',2),
                   'RMYRTD_T':('HV',3),
                   'Rotronics_Fan_rpm':('F',0),
                   'RMYRTD_Fan_rpm':('F',1),
                   }

if '__main__' == __name__:

    print('use storage.storage2.create_table() instead.')
    exit()




    
    for table in sorted(conf):
        print('- - -')
        print table
        for column in conf[table]:
            assert 'dbtag' in column
            # everything else is optional. dbtype default to DOUBLE
            print('\t' + column['dbtag'])

    import MySQLdb
    from os.path import expanduser
    password = open(expanduser('~/mysql_cred')).read().strip()
    dbname = 'kmetlog'
    conn = MySQLdb.connect(host='localhost',
                                 user='root',
                                 passwd=password,
                                 db=dbname)
    cur = conn.cursor()

    # conf: a dictionary; one table per key;
    # each key maps to a list of dictionaries: {'dbtag':...} is mandatory; everything else is optional.
    # 'dbtype' defaults to DOUBLE

    for table in sorted(conf):
        tmp = ','.join([' '.join(tmp) for tmp in [(column['dbtag'],column.get('dbtype','DOUBLE')) for column in conf[table]]])
        cmd = 'CREATE TABLE IF NOT EXISTS {} ({})'.format('{}.`{}`'.format(dbname,table),tmp)
        print(cmd)
        #cur.execute(cmd)
