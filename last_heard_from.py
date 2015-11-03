#!/usr/bin/python
#
# Query the database to see when each node was last heard from
# (for only those in the database)
#
# Stanley Lio, hlio@soest.hawaii.edu
import storage,re,traceback,math,time
from os.path import exists
from datetime import datetime
from storage.storage import storage_read_only


dbfile = './storage/sensor_data.db'
if not exists(dbfile):
    dbfile = '../data/base-003/storage/sensor_data.db'
    #dbfile = '../data/base-004/storage/sensor_data.db'
    #dbfile = '../data/node-005/storage/sensor_data.db'
    #dbfile = '../data/node-019/storage/sensor_data.db'

store = storage_read_only(dbfile=dbfile)

nodes = [int(t[5:8]) for t in store.get_list_of_tables() if re.match('node_\d{3}',t)]


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
            ago = (datetime.now() - t).total_seconds()
            print 'node {}:\t{:.0f}d {:2.0f}:{:02.0f}:{:02.0f} ago'.\
                  format(node_id,ago//(3600*24),(ago%(3600*24))//3600,(ago%3600)//60,ago%60)
            #print 'node {}:\t{:2.0f}:{:02.0f}:{:02.0f} ago'.\
            #      format(node_id,(ago%(3600*24))//3600,(ago%3600)//60,ago%60)
        except TypeError:
            #traceback.print_exc()
            pass
        except:
            traceback.print_exc()

    time.sleep(1)

