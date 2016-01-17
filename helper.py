import time
from datetime import datetime

def dt2ts(dt):
    return time.mktime(dt.timetuple()) + (dt.microsecond)*(1e-6)

def ts2dt(ts):
    return datetime.fromtimestamp(ts)

'''def get_dbfile(base=None,node=None):
    if 'base-003' == base:
        return '/home/nuc/node/storage/sensor_data.db'
    if 'node-005' == node:
        return '/home/nuc/data/node-005/storage/sensor_data.db'
    if 'node-019' == node:
        return '/home/nuc/data/node-019/storage/sensor_data.db'
    raise'''

def get_dbfile(site,node_id=None):
    if 'poh' == site:
        return '/home/nuc/node/storage/sensor_data.db'
    if 'msb228' == site:
        if 'node-005' == node_id:
            return '/home/nuc/data/node-005/storage/sensor_data.db'
        elif 'node-019' == node_id:
            return '/home/nuc/data/node-019/storage/sensor_data.db'
    return None
