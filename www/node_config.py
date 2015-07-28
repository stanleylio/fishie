#!/usr/bin/python
import cgi,cgitb,sys,json
sys.path.append('../storage')
sys.path.append('../config')
from config_support import *
from storage import storage_read_only
from datetime import datetime
import time

#import cgi
#cgi.test()

cgitb.enable(display=1)
form = cgi.FieldStorage()

#print 'Content-Type: text/plain; charset=utf8'
print 'Content-Type: application/json; charset=utf8'
print

#print form.getlist('p')
#exit()

d = {}

# http://192.168.1.102/node_config.py?p=list_of_nodes
# get the list of nodes of which the database has data
if 'list_of_nodes' in form.getlist('p'):
    store = storage_read_only()
    nodes = []
    time_col = 'ReceptionTime'
    for node_id in read_capabilities().keys():
        r = store.read_last_N(node_id,time_col,1)
        if r is not None:
            nodes.append(node_id)
    d.update({'list_of_nodes':nodes})

# http://192.168.1.102/node_config.py?p=list_of_variables&id=4
if 'list_of_variables' in form.getlist('p'):
    tags = read_capabilities()[int(form.getlist('id')[0])]['tag']
    d.update({'list_of_variables':tags})

# get the latest sample of all variables (tags/columns) in the database
# http://192.168.1.102/node_config.py?p=latest_sample&id=4
if 'latest_sample' in form.getlist('p'):
    node_id = int(form.getlist('id')[0])
    #if is_base():
    time_col = 'ReceptionTime'
    store = storage_read_only()
    r = store.read_last_N(node_id,time_col,1)

    # replaced the (tuple of one element) with the element itself
    if r is not None:
        for k,v in r.iteritems():
            r[k] = v[0]
            # convert python datetime to posix timestamps
            if type(r[k]) is datetime:
                r[k] = time.mktime(r[k].timetuple())
    d.update({'latest_sample':r})

# get a dict of tag:unit mapping (for all tags defined in config file)
# http://192.168.1.102/node_config.py?p=units&id=4
if 'units' in form.getlist('p'):
    node_id = int(form.getlist('id')[0])
    tags = get_tag(node_id)
    units = get_unit(node_id)
    d.update({'units':dict(zip(tags,units))})

# http://192.168.1.102/node_config.py?p=list_of_disp_vars&id=4
if 'list_of_disp_vars' in form.getlist('p'):
    node_id = int(form.getlist('id')[0])
    r = get_list_of_disp_vars(node_id)
    d.update({'list_of_disp_vars':r})

# http://192.168.1.102/node_config.py?p=node_name&id=4
if 'node_name' in form.getlist('p'):
    tmp = form.getlist('id')
    if len(tmp) > 0:
        d.update({'node_name':get_name('node_{:03d}'.format(tmp[0]))})
    else:
        d.update({'node_name':get_name()})

# http://192.168.1.102/node_config.py?p=node_note&id=4
if 'node_note' in form.getlist('p'):
    tmp = form.getlist('id')
    if len(tmp) > 0:
        d.update({'node_note':get_note('node_' + tmp[0])})
    else:
        d.update({'node_note':get_note()})

# http://192.168.1.102/node_config.py?p=node_id
if 'node_id' in form.getlist('p'):
    #if is_node():
    d.update({'node_id':get_node_id()})

jsonstr = json.dumps(d,separators=(',',':'))
print jsonstr

