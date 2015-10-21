#!/usr/bin/python
import cgi,cgitb,json,time,sys
sys.path.append('../../')
sys.path.append('../../storage')
sys.path.append('../../config')
from storage import storage_read_only
from config_support import *
from datetime import timedelta

cgitb.enable(display=1)

print 'Content-Type: application/json; charset=utf8'
print

form = cgi.FieldStorage()
# use node_id of THIS node if not specified in the AJAX GET request
if is_node():
    node_id = get_node_id()
elif is_base():
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

store = storage_read_only()

name = get_name()
note = get_note()
if note is None:
    note = ''
if is_node():
    time_col = 'Timestamp'
elif is_base():
    time_col = 'ReceptionTime'

# get the unit of the variable
tags = get_tag(node_id)
units = get_unit(node_id)
mapping = dict(zip(tags,units))
unit = mapping[tag]

# get the description of the variable
tags = get_tag(node_id)
descriptions = get_description(node_id)
mapping = dict(zip(tags,descriptions))
description = mapping[tag]

#avg = None
#if nhour > 24*7:
#    avg = 'hourly'
#retrieved = store.read(node_id,time_col=time_col,variables=[tag],nhour=nhour,avg=avg)
retrieved = store.read_time_range(node_id,time_col,[time_col,tag],timedelta(hours=nhour))
ts = tuple(time.mktime(t.timetuple()) for t in retrieved[time_col])
dp = retrieved[tag]
tp = zip(ts,dp)

tmp = {'id':node_id,
       'node_name':name,
       'node_note':note,
       'tag':tag,
       'unit':unit,
       'description':description,
       'points':json.dumps(tp,separators=(',',':'))}

jsonstr = json.dumps(tmp,separators=(',',':'))
print jsonstr
