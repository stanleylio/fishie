#!/usr/bin/python
# "Query Latest Non-null Reading"
#
# Example:
# http://192.168.0.20/qlnr.py?site=poh&node_id=node-003&var=ec
#
# Stanley Lio, hlio@hawaii.edu
# Januray 2016
import cgi,cgitb,json,sys
sys.path.append('..')
import storage
from storage.storage import storage_read_only,auto_time_col
from helper import dt2ts,get_dbfile

#cgitb.enable(display=1)
form = cgi.FieldStorage()

site = form.getlist('site')[0]
node = form.getlist('node_id')[0]
var = form.getlist('var')[0]

store = storage_read_only(dbfile=get_dbfile(site,node))
time_col = auto_time_col(store,node)
tmp = store.read_latest_non_null(node,time_col,var)

d = {'site':site,
     'node':node,
     'var':var,
     time_col:dt2ts(tmp[time_col]),
     var:tmp[var]}

jsonstr = json.dumps(d,separators=(',',':'))
#print 'Content-Type: text/plain; charset=utf8'
print 'Content-Type: application/json; charset=utf8'
print
print jsonstr
