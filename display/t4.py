# humidity in RM228
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
time_col = 'Timestamp'
tmp = [time_col,'RH_HTU21D']
d = store.read_time_range(node_id=5,time_col=time_col,cols=tmp,timerange=timedelta(days=30))
d['RH_HTU21D'] = [float('NaN') if n is None else n for n in d['RH_HTU21D']]
d5 = {'x':d[time_col],'y':d['RH_HTU21D'],'linelabel':'styroform'}

dbfile = '/home/nuc/data/node-019/storage/sensor_data.db'
store = storage_read_only(dbfile=dbfile)
time_col = 'Timestamp'
tmp = [time_col,'RH_HTU21D']
d = store.read_time_range(node_id=19,time_col=time_col,cols=tmp,timerange=timedelta(days=30))
d['RH_HTU21D'] = [float('NaN') if n is None else n for n in d['RH_HTU21D']]
d19 = {'x':d[time_col],'y':d['RH_HTU21D'],'linelabel':'slpersonal'}

data = [d5,d19]

fn = '/home/nuc/node/www/t4/rh.png'
plot_multi_time_series(data,fn,title='Humidity in MSB RM228 (HTU21D)',ylabel='%RH')
