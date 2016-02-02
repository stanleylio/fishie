import calendar
from datetime import datetime
from numpy import diff,mean,median,size,flatnonzero,append,insert

def dt2ts(dt):
    return calendar.timegm(dt.timetuple()) + (dt.microsecond)*(1e-6)

def ts2dt(ts):
    return datetime.fromtimestamp(ts)

# I don't like this...
def get_dbfile(site,node_id=None):
    if 'poh' == site:
        return '/home/nuc/node/www/poh/storage/sensor_data.db'
    if 'msb228' == site:
        if 'node-005' == node_id:
            return '/home/nuc/data/node-005/storage/sensor_data.db'
        elif 'node-019' == node_id:
            return '/home/nuc/data/node-019/storage/sensor_data.db'
    return None

# processing/analysis stuff
def split_by_group(t,x):
    tmp = diff(t)
    #tmp = absolute(diff(t))
    I = flatnonzero(tmp > mean(tmp)) + 1;
    start = insert(I,0,0)
    stop = append(I,size(t))

    t = [[t[i[0]:i[1]]] for i in zip(start,stop)]
    x = [[x[i[0]:i[1]]] for i in zip(start,stop)]
    return t,x

def median_of_group(t,x):
    t,x = split_by_group(t,x)
    t = [mean(tt) for tt in t]
    x = [median(xx) for xx in x]
    return t,x

