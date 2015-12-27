# temperature sensor comparison (silcon in styrofoam)
#
# Stanley Lio, hlio@soest.hawaii.edu
# December 2015
import sys,traceback
sys.path.append('..')
from datetime import timedelta
from storage.storage import storage_read_only
from gen_plot import plot_multi_time_series

dbfile = '/home/nuc/data/node-005/storage/sensor_data.db'
store = storage_read_only(dbfile=dbfile)

for node in store.get_list_of_tables():
    print node
    #for t in store.get_list_of_columns(node):
    #    print '\t' + t
    print '\t' + ','.join(store.get_list_of_columns(node))

# - - - - -

time_col = 'Timestamp'
T = ['T_5803','T_180','T_280','T_9808','T_HTU21D']

tmp = list(T)
tmp.append(time_col)
d = store.read_time_range(node_id=5,time_col=time_col,cols=tmp,timerange=timedelta(days=60))

def nanize(y,convf=lambda (x): x):
    return [float('NaN') if n is None else convf(n) for n in d[k]]

print d.keys()
data = [{'x':d[time_col],'y':nanize(d[k]),'linelabel':k} for k in d.keys() if k != time_col]
fn = '/home/nuc/node/www/t3/temperature.png'
plot_multi_time_series(data,fn,title='Temperature (sensor-in-a-styrofoam-box)',ylabel='Deg.C')

