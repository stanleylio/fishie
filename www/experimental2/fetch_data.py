#!/usr/bin/python
import cgi,cgitb,json,time,sys
sys.path.append('../../')
sys.path.append('../../storage')
from storage import storage
from config_support import get_node_id,get_name,get_note,get_unit,tag2description,get_color

cgitb.enable(display=1)

print 'Content-Type: application/json; charset=utf8'
print

form = cgi.FieldStorage()
# use node_id of THIS node if not specified in the AJAX GET request
node_id = get_node_id()
try:
    node_id = int(form.getlist('id')[0])
except:
    pass
tag = form.getlist('tag')[0]
# default 1 hr of data, if not specified otherwise
nhour = 1
try:
    nhour = float(form.getlist('nhour')[0])
except:
    pass

store = storage()

name = get_name()
note = get_note()
if note is None:
    note = ''
time_col = 'Timestamp'
unit = get_unit(node_id,tag)
description = tag2description(node_id,tag)
linecolor = get_color(node_id,tag)

avg = None
if nhour > 24*7:
    avg = 'hourly'
retrieved = store.read(node_id,time_col=time_col,variables=[tag],nhour=nhour,avg=avg)
ts = tuple(time.mktime(t.timetuple()) for t in retrieved[time_col])
dp = retrieved[tag]
tp = zip(ts,dp)

tmp = {'id':node_id,
       'node_name':name,
       'node_note':note,
       'tag':tag,
       'unit':unit,
       'description':description,
       'linecolor':linecolor,
       'points':json.dumps(tp,separators=(',',':'))}

jsonstr = json.dumps(tmp,separators=(',',':'))
print jsonstr
