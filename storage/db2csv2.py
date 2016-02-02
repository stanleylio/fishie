# Stanley Lio, hlio@hawaii.edu
# February 2016
import calendar,sqlite3

def dt2ts(dt):
    return calendar.timegm(dt.timetuple()) + (dt.microsecond)*(1e-6)

def ts2dt(ts):
    return datetime.fromtimestamp(ts)


table = 'node_009'
time_col = 'ReceptionTime'
cols = [time_col,'d2w']
dbfile = 'sensor_data.db'

cmd = 'SELECT {cols} FROM {table}'.format(cols=','.join(cols),table=table)
print cmd
conn = sqlite3.connect(dbfile,\
                            detect_types=sqlite3.PARSE_DECLTYPES |\
                            sqlite3.PARSE_COLNAMES)
c = conn.cursor()
c.execute('PRAGMA journal_mode = WAL')
c.row_factory = sqlite3.Row
c.execute(cmd)
tmp = c.fetchall()
tmp = {v:tuple(r[v] for r in tmp) for v in cols}

# convert Python datetime to POSIX timestamps
tmp[time_col] = tuple(dt2ts(v) for v in tmp[time_col])

print len(tmp[time_col]), 'entries'

print 'Writing to file...'
with open('{}.csv'.format(table),'w',0) as f:
    f.write(','.join(cols) + '\n')
    for r in zip(*[tmp[v] for v in cols]):
        f.write(','.join([str(t) for t in r]) + '\n')
print 'Done.'

