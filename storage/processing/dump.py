import traceback
from storage import storage_read_only
from helper import *
from os import makedirs
from os.path import join


store = storage_read_only()
for table in store.get_list_of_tables():
    try:
        makedirs('output')
    except:
        pass
    
    tmp = store.read_all(table)
    if tmp is not None:
        # convert Python datetime to POSIX timestamps
        for time_col in ['ReceptionTime','Timestamp']:
            try:
                tmp[time_col] = tuple(dt2ts(v) for v in tmp[time_col])
            except:
                traceback.print_exc()

        # ah the one-liner disease...
        with open(join('output',table + '.csv'),'w') as f:
            f.write(','.join(tmp.keys()) + '\n')
            f.write('\n'.join([','.join([str(v) for v in r]) for r in zip(*[tmp[k] for k in tmp.keys()])]))
    else:
        print('table {} is empty'.format(table))
