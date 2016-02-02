import calendar,json
from storage import storage_read_only

def dt2ts(dt):
    return calendar.timegm(dt.timetuple()) + (dt.microsecond)*(1e-6)

node = 'node-009'

store = storage_read_only()
tmp = store.read_all(node)

# convert Python datetime to POSIX timestamps
time_col = 'Timestamp'
if 'ReceptionTime' in tmp:
    time_col = 'ReceptionTime'
tmp[time_col] = tuple(dt2ts(v) for v in tmp[time_col])

print 'Writing to file...'
with open(node + '.json','w') as f:
    json.dump(tmp,f,separators=(',',':'))
print 'Done.'
