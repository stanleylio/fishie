import calendar
from storage import storage_read_only

def dt2ts(dt):
    return calendar.timegm(dt.timetuple()) + (dt.microsecond)*(1e-6)

node = 'node-011'

store = storage_read_only()
tmp = store.read_all(node)

# need it for the ordering
cols = store.get_list_of_columns(node)

# convert Python datetime to POSIX timestamps
time_col = cols[0]  # the first column is time - a convention so far maintained
tmp[time_col] = tuple(dt2ts(v) for v in tmp[time_col])

# ah the one-liner sickness...
with open(node + '.csv','w') as f:
    f.write(','.join(cols) + '\n')
    f.write('\n'.join([','.join([str(v) for v in r]) for r in zip(*[tmp[k] for k in cols])]))

