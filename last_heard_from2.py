#!/usr/bin/python
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2017
from storage.storage2 import storage,auto_time_col
import time,traceback
from datetime import timedelta


time_cols = ['ReceptionTime','Timestamp','ts']
store = storage()

while True:
    print('\x1b[2J\x1b[;H')
    for table in store.get_list_of_tables():
        columns = store.get_list_of_columns(table)
        time_col = auto_time_col(columns)
        max_t = -1
        for column in set(columns) - set(time_cols):
            try:
                r = store.read_latest_non_null(table,time_col,column)
                if r[time_col] > max_t:
                    max_t = r[time_col]
            except:
                #traceback.print_exc()
                pass
        if max_t < 0:
            print('{} (no data)'.format(table))
            continue
        print table,timedelta(seconds=time.time() - max_t)
    time.sleep(5)
exit()








import storage,re,traceback,time,sys
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
            print '{}:\t{:.0f}d {:2.0f}:{:02.0f}:{:02.0f} ago'.\
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

