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
