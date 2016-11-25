# goal: get rid of this whole file.
import calendar
from datetime import datetime
from numpy import diff,mean,median,size,flatnonzero,append,insert,absolute


def dt2ts(dt=None):
    if dt is None:
        dt = datetime.utcnow()
    return calendar.timegm(dt.timetuple()) + (dt.microsecond)*(1e-6)

def ts2dt(ts=None):
    if ts is None:
        ts = dt2ts()
    return datetime.utcfromtimestamp(ts)


# processing/analysis stuff

# should it first check whether the data are indeed in groups?
# or at least emit a warning if they aren't?
def split_by_group(t,x):
    """returns a list of groups; each group contains samples
that are close to each other in time"""
    assert len(t) == len(x)
    
    #tmp = diff(t)
    #tmp = absolute(diff(t))

    p = sorted(zip(t,x),key=lambda x: x[0])
    t,x = zip(*p)
    tmp = diff(t)
    
    I = flatnonzero(tmp > mean(tmp)) + 1;
    start = insert(I,0,0)
    stop = append(I,size(t))

    t = [[t[i[0]:i[1]]] for i in zip(start,stop)]
    x = [[x[i[0]:i[1]]] for i in zip(start,stop)]
    return t,x

def median_of_group(t,x):
    """Timestamps can be datetime.datetime or POSIX floats"""
    assert len(t) == len(x)

    ttype = type(t[0])
    #if isinstance(t[0],float):
    if ttype is float:
        pass
    elif ttype is datetime:
        t = [dt2ts(tmp) for tmp in t]
    else:
        assert False,'Timestamps should either be datetime or POSIX floats'
    
    t,x = split_by_group(t,x)
    t = [mean(tmp) for tmp in t]
    x = [median(tmp) for tmp in x]

    if ttype is datetime:
        t = [ts2dt(tmp) for tmp in t]
    return t,x

def loadcsv(fn,hasheader=True):
    with open(fn,'r') as f:
        tags = f.readline().strip().split(',')

    from numpy import loadtxt
    if hasheader:
        r = loadtxt(fn,delimiter=',',skiprows=1)
    else:
        r = loadtxt(fn,delimiter=',')
    r = zip(*r)

    return {r[0]:r[1] for r in zip(tags,r)}

def savecsv(fn,d,keys=None):
    if not all([len(d[d.keys()[0]]) == len(d[k]) for k in d.keys()]):
        print('Column length do not match.')
        assert False
    with open(fn,'w') as f:
        if keys is None:
            keys = d.keys()
        f.write(','.join([k.replace(',','') for k in keys]) + '\n')
        f.write('\n'.join([','.join([str(rr) for rr in r]) for r in zip(*[d[k] for k in keys])]))

'''def plot1(x,y,title='',xlabel='',ylabel='',linelabel='',color='b',style='.',fn=None):
    """Plot a single-var time series"""
    from matplotlib import pyplot
    from matplotlib.font_manager import FontProperties
    fontP = FontProperties()
    fontP.set_size('small')
    
    fig,ax = pyplot.subplots()
    ax.plot(x,y,style,color=color,label=linelabel)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)

    if linelabel is not None and len(linelabel) > 0:
        h,l = ax.get_legend_handles_labels()
        ax.legend(h,l,loc='upper left',prop=fontP)

    if isinstance(x[0],datetime):
        fig.autofmt_xdate()

    if fn is not None:
        fig.savefig(fn)
    return fig'''


#def m2ft(m):
#    return m*100./2.54/12.

#def c2f(c):
#    return c*9./5. + 32.


'''# I don't like this... but the config has to live somewhere
def get_dbfile(site,node_id=None):
    """where to locate the db for the given site. Pure black magic."""
    if 'poh' == site:
        # He`eia fishpond
        return '/home/nuc/node/www/poh/storage/sensor_data.db'
    elif 'coconut' == site:
        if 'node-026' == node_id:
            # Hollie's water tanks
            return '/home/nuc/data/htank/storage/sensor_data.db'
        else:
            # I don't think this is active
            return '/home/nuc/node/www/coconut/storage/sensor_data.db'
    elif 'msb228' == site:
        # MSB228 nodes
        if 'node-019' == node_id:
            return '/home/nuc/data/node-019/storage/sensor_data.db'
        #elif 'node-005' == node_id:
            #return '/home/nuc/data/node-005/storage/sensor_data.db'
    return None'''

