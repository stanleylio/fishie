#!/usr/bin/python
#
# show the reception time of the latest message from each node
# by querying the database.
#
# Stanley H.I. Lio
# hlio@soest.hawaii.edu
import storage,re,traceback,time
from os.path import exists,expanduser
sys.path.append(expanduser('~'))
from datetime import datetime
from time import sleep
from node.storage.storage import storage_read_only


dbfile = './storage/sensor_data.db'
if not exists(dbfile):
    dbfile = '/var/uhcm/storage/sensor_data.db'
    #dbfile = '../data/base-004/storage/sensor_data.db'
    #dbfile = '../data/node-005/storage/sensor_data.db'
    #dbfile = '../data/node-019/storage/sensor_data.db'

store = storage_read_only(dbfile=dbfile)

nodes = [t.replace('_','-') for t in store.get_list_of_tables() if re.match('^node,*',t)]


while True:
    print('\x1b[2J\x1b[;H')
    
    print('From {}'.format(dbfile))
    print('Last heard from (days hh:mm:ss)...')
    #print('Last heard from (hh:mm:ss)...')
    for node_id in nodes:
        try:
            time_col = 'Timestamp'
            if 'ReceptionTime' in store.get_list_of_columns(node_id):
                time_col = 'ReceptionTime'
            t = store.read_last_N(node_id,time_col)[time_col][0]
            ago = (datetime.utcnow() - t).total_seconds()
            print 'node {}:\t{:.0f}d {:2.0f}:{:02.0f}:{:02.0f} ago'.\
                  format(node_id,ago//(3600*24),(ago%(3600*24))//3600,(ago%3600)//60,ago%60)
            #print 'node {}:\t{:2.0f}:{:02.0f}:{:02.0f} ago'.\
            #      format(node_id,(ago%(3600*24))//3600,(ago%3600)//60,ago%60)
        except KeyboardInterrupt:
            print 'user interrupted'
            exit()
        except TypeError:
            #traceback.print_exc()
            pass
        except:
            traceback.print_exc()

    time.sleep(5)

