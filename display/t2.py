# plot BMP180 data on base-001
#
# Stanley Lio, hlio@hawaii.edu
# December 2015
import traceback,sys
sys.path.append(r'..')
from datetime import datetime,timedelta
from gen_plot import plot_time_series
from helper import *


with open('/home/nuc/data/base-001/log/base_temperature.txt') as f:
    d = [line.strip('\s\x00').split(',') for line in f]
    ddd = []
    for dd in d:
        try:
            ddd.append([ts2dt(float(dd[0])),float(dd[1])/1e3,float(dd[2])])
        except ValueError:
            pass
    #d = zip(*ddd)

    d = []
    for k,v in enumerate(ddd):
        if v[0] >= datetime.utcnow() + timedelta(days=-30) and\
           v[0] > ddd[k-1][0]:
            d.append(v)
    d = zip(*d)


'''with open('/home/nuc/data/base-001/log/base_temperature.txt') as f:
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
t = d[2]'''

bdir = '/home/nuc/node/www/t2/'

plot_time_series(d[0],d[1],bdir + 'base_p.png',
                 title='Barometric Pressure (Base Station BMP180)',
                 xlabel='Time',ylabel='kPa')


plot_time_series(d[0],d[2],bdir + 'base_t.png',
                 title='Base Station Temperature',
                 xlabel='Time',ylabel='Deg.C')

