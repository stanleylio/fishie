import calendar
from datetime import datetime
from numpy import diff,mean,median,size,flatnonzero,append,insert,absolute
from matplotlib import pyplot

def dt2ts(dt):
    return calendar.timegm(dt.timetuple()) + (dt.microsecond)*(1e-6)

def ts2dt(ts):
    return datetime.utcfromtimestamp(ts)

#def m2ft(m):
#    return m*100./2.54/12.

#def c2f(c):
#    return c*9./5. + 32.

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

'''def gen_table(t):
    """Create an HTML table given a list of lists as rows for the table.
    First row is the table header."""
    s = u'<thead><tr>{}</tr></thead>'.format(u''.join([u'<th>{}</th>'.format(f) for f in t[0]]))
    body = ''
    for row in t[1:]:
        body = body + u'<tr>{}</tr>'.format(''.join([u'<td>{}</td>'.format(f) for f in row]))
    s = s + u'<tbody>{}</tbody>'.format(body)
    s = u'<table>{}</table>'.format(s)
    return s'''

# processing/analysis stuff

# should it check first whether they data are indeed in groups?
# or at least emit a warning if they aren't?
def split_by_group(t,x):
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
        print('WARNING: Columns are not of the same length.')
        assert False
    with open(fn,'w') as f:
        if keys is None:
            keys = d.keys()
        f.write(','.join([k.replace(',','') for k in keys]) + '\n')
        f.write('\n'.join([','.join([str(rr) for rr in r]) for r in zip(*[d[k] for k in keys])]))

def plot1(x,y,title='',xlabel='',ylabel='',linelabel='',color='b',style='.',fn=None):
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
    return fig


