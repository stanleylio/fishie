#!/usr/bin/python
# Query for data within a time range
#
# Parameters:
#   base: base station ID
#   node: node ID
#   variable: name of the variable (e.g. P_5803)
#   begin: start of the time range
#   end: end of the time range
#
# Example:
# http://192.168.0.20/qtr.py?site=poh&node_id=node-004&var=T_180&begin=1451540771&end=1451627216
#
# Stanley Lio, hlio@hawaii.edu
# Januray 2016
import cgi,cgitb,sys,json,time,traceback
sys.path.append('..')
import config,storage
from config.config_support import *
from storage.storage import storage_read_only,auto_time_col
from os.path import exists
from helper import dt2ts,ts2dt,get_dbfile

#import cgi
#cgi.test()
cgitb.enable(display=1)
form = cgi.FieldStorage()
#print form.getlist('p')
#exit()


# (base ID,node ID,variable name,time range)
site = form.getlist('site')[0]
node = form.getlist('node_id')[0]
#node = node.replace('-','_')    # '-' is illegal in a table's name
var = form.getlist('var')[0]
begin = form.getlist('begin')[0]
begin = ts2dt(float(begin))
# "end" is optional. "til this moment" if not specified.
try:
    end = form.getlist('end')[0]
    end = ts2dt(float(end))
except:
    end = None

#print site,node,var,begin,end

store = storage_read_only(dbfile=get_dbfile(site,node))
time_col = auto_time_col(store,node)
cols = [time_col,var]
r = store.read_time_range(node,time_col,cols,begin,end=end)
# POSIX timestamps
r[time_col] = tuple(dt2ts(t) for t in r[time_col])
# plotly.js's preferred format (ISO)
#r[time_col] = tuple(str(t) for t in r[time_col])
#print r
d = {'qtr':r}

jsonstr = json.dumps(d,separators=(',',':'))
#print 'Content-Type: text/plain; charset=utf8'
print 'Content-Type: application/json; charset=utf8'
print
print jsonstr
