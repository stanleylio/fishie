# Stanley Lio, hlio@hawaii.edu
# February 2016
import calendar,sqlite3,json

def dt2ts(dt):
    return calendar.timegm(dt.timetuple()) + (dt.microsecond)*(1e-6)

def ts2dt(ts):
    return datetime.fromtimestamp(ts)


table = 'node_009'
time_col = 'ReceptionTime'
cols = [time_col,'d2w']
dbfile = 'sensor_data.db'

cmd = 'SELECT {cols} FROM {table}'.format(cols=','.join(cols),table=table)
#cmd = 'SELECT {cols} FROM {table} ORDER BY {time_col} DESC LIMIT 3000'.format(cols=','.join(cols),table=table,time_col=time_col)
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
tmp = zip(*[tmp[k] for k in cols])
tmp = sorted(tmp,key=lambda x: x[0])
tmp = zip(*tmp)
tmp = {v:tmp[k] for k,v in enumerate(cols)}

# sort by time_col... wait what? Order shouldn't matter
#tmp = {k:sorted(tmp[k],key=lambda x: tmp[time_col],reverse=False) for k in tmp.keys()}

#assert tmp[time_col][-1] > tmp[time_col][0]

print len(tmp[time_col]), 'entries'

print 'Writing to file...'
with open(table + '.json','w') as f:
    json.dump(tmp,f,separators=(',',':'))
print 'Done.'
