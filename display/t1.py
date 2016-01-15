# Combined plots - all T_180 on one plot, all P_5803 on one plot, etc.
#
# Stanley Lio, hlio@soest.hawaii.edu
# December 2015
import sys,traceback
sys.path.append('..')
from datetime import timedelta
from storage.storage import storage_read_only
from gen_plot import plot_multi_time_series

def haha(c):
    time_col = c['time_col']
    tag = c['tag']
    nodes = c['nodes']
    timerange = c['timerange']
    title = c['title']
    ylabel = c['ylabel']
    try:
        convf = c['convf']
    except:
        convf = lambda (x): x

    print '- - -'
    print tag
    data = []
    for node in nodes:
        try:
            print node
            tmp = store.read_past_time_period(node_id=node,time_col=time_col,cols=[time_col,tag],
                                        timerange=timerange)
            x = tmp[time_col]
            y = tmp[tag]
            y = [float('NaN') if n is None else convf(n) for n in y]
            data.append({'x':x,'y':y,'linelabel':node})
        except:
            traceback.print_exc()
            pass

    fn = '/home/nuc/node/www/t1/' + tag + '.png'
    plot_multi_time_series(data,fn,
                     title=title,
                     ylabel=ylabel)


#dbfile = '../storage/sensor_data.db'
dbfile = '../storage/bounded/sensor_data.db'
store = storage_read_only(dbfile=dbfile)

for node in store.get_list_of_tables():
    print node
    #for t in store.get_list_of_columns(node):
    #    print '\t' + t
    print '\t' + ','.join(store.get_list_of_columns(node))

# - - - - -

C = []

C.append({'time_col':'ReceptionTime',
          'tag':'P_180',
          'nodes':['node-001','node-002','node-003','node-004'],
          'timerange':timedelta(days=90),
          'title':'Barometric Pressure (BMP180, P_180)',
          'ylabel':'kPa',
          'convf':lambda (x): x/1000.0})

C.append({'time_col':'ReceptionTime',
'tag':'T_180',
'nodes':['node-001','node-002','node-003','node-004'],
'timerange':timedelta(days=90),
'title':'Casing Temperature (BMP180, T_180)',
'ylabel':'Deg.C'})

C.append({'time_col':'ReceptionTime',
'tag':'P_5803',
'nodes':['node-001','node-002','node-003','node-004'],
'timerange':timedelta(days=90),
'title':'Water Pressure (MS5803-14BA, P_5803)',
'ylabel':'kPa'})

C.append({'time_col':'ReceptionTime',
'tag':'T_5803',
'nodes':['node-001','node-002','node-003','node-004'],
'timerange':timedelta(days=90),
'title':'Water Temperature (MS5803-14BA, T_5803)',
'ylabel':'Deg.C'})

C.append({'time_col':'ReceptionTime',
'tag':'Temperature',
'nodes':['node-001','node-002','node-003','node-004'],
'timerange':timedelta(days=90),
'title':'Water Temperature (Aanderaa 4330F, Temperature)',
'ylabel':'Deg.C'})

C.append({'time_col':'ReceptionTime',
'tag':'O2Concentration',
'nodes':['node-001','node-002','node-003','node-004'],
'timerange':timedelta(days=90),
'title':'O2 Concentration (Aanderaa 4330F, O2Concentration)',
'ylabel':'uM'})

C.append({'time_col':'ReceptionTime',
'tag':'AirSaturation',
'nodes':['node-001','node-002','node-003','node-004'],
'timerange':timedelta(days=90),
'title':'Air Saturation (Aanderaa 4330F, AirSaturation)',
'ylabel':'%'})

C.append({'time_col':'ReceptionTime',
'tag':'ec',
'nodes':['node-001','node-002','node-003','node-004'],
'timerange':timedelta(days=90),
'title':'Conductivity (EZO EC, ec)',
'ylabel':'uS'})


for c in C:
    haha(c)


