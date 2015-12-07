# plot BMP180 data on base-001
# Stanley Lio, hlio@hawaii.edu
# December 2015
import traceback
from datetime import datetime
from gen_plot import plot_time_series


def dt2ts(dt):
    return time.mktime(dt.timetuple()) +\
                 (dt.microsecond)*(1e-6)

def ts2dt(ts):
    return datetime.fromtimestamp(ts)


with open('/home/nuc/data/base-001/log/base_temperature.txt') as f:
    d = [line.strip('\s\x00').split(',') for line in f]
    d = zip(*[[float(b) for b in c] for c in d])
    d = [list(c) for c in d]

for k,v in enumerate(d[0]):
    if v < d[0][k-1]:
        print v
        d[0][k] = d[0][k+1]
        d[1][k] = float('nan')
        d[2][k] = float('nan')


ts = tuple(ts2dt(t) for t in d[0])
p = tuple(c/1e3 for c in d[1])
t = d[2]

bdir = '/home/nuc/node/www/t2/'

plot_time_series(ts,p,bdir + 'base_p.png',
                 title='Barometric Pressure (Base Station BMP180)',
                 xlabel='Time',ylabel='kPa')


plot_time_series(ts,t,bdir + 'base_t.png',
                 title='Base Station Temperature',
                 xlabel='Time',ylabel='Deg.C')

print min(ts)
print max(ts)


