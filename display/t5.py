import sys,traceback
sys.path.append('..')
from datetime import datetime,timedelta
from storage.storage import storage_read_only
from gen_plot import plot_multi_time_series
from os import makedirs


dbfile = '/home/nuc/node/storage/sensor_data.db'
store = storage_read_only(dbfile=dbfile)
time_col = 'ReceptionTime'
v = 'd2w'
cols = [time_col,v]

# "20160115 1350    218 cm to cone rim, 122~130 cm water depth, node-008 (us1)"
#begin = datetime(2016,01,15,23,40)
#end = datetime(2016,01,16,00,10)

# "20160115 1404    110cm to cone rim, 35 cm water depth, node-009 (us2)"
#begin = datetime(2016,01,15,23,55)
#end = datetime(2016,01,16,00,10)

# "20160115 1329    110 cm to cone rim, 37 cm water depth, node-009 (us2)"
#begin = datetime(2016,01,15,23,20)
#end = datetime(2016,01,15,23,40)

#d = store.read_time_range('node-008',time_col,cols,begin,end)
d = store.read_past_time_period(node_id='node-008',time_col=time_col,
                                cols=cols,timerange=timedelta(days=7))
def f(v):
    # sensor_length + sensor_rim_to_cinder_block = sensor_measurement + water_depth
    # water_depth = sensor_length + sensor_rim_to_cinder_block - sensor_measurement
    return (50.7 + 2180 - v)/10.
d[v] = [float('NaN') if n is None else f(n) for n in d[v]]
d[v] = [float('NaN') if n < 0 else n for n in d[v]]
us1 = {'x':d[time_col],'y':d[v],'linelabel':'Makaha 2 (node-008, us1)'}

d = store.read_past_time_period(node_id='node-009',time_col=time_col,
                                cols=cols,timerange=timedelta(days=7))
#d = store.read_time_range('node-009',time_col,cols,begin,end)
def f(v):
    return (50.7 + 1100 - v)/10.
d[v] = [float('NaN') if n is None else f(n) for n in d[v]]
d[v] = [float('NaN') if n < 0 else n for n in d[v]]
us2 = {'x':d[time_col],'y':d[v],'linelabel':'Makaha 1 (node-009, us2)'}

data = [us1,us2]

try:
    makedirs('/home/nuc/node/www/t5')
except:
    pass
fn = '/home/nuc/node/www/t5/us.png'
plot_multi_time_series(data,fn,title='Makaha Water Depth',ylabel='cm')
