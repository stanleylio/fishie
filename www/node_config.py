#!/usr/bin/python
#
# Stanley Lio, hlio@hawaii.edu
# Januray 2016
import cgi,cgitb,sys,json,time,traceback
sys.path.append('..')
import config,storage
from config.config_support import *
from storage.storage import storage_read_only
from datetime import datetime
from os.path import exists
from helper import dt2ts,ts2dt,get_dbfile,auto_time_col

#import cgi
#cgi.test()
cgitb.enable(display=1)
form = cgi.FieldStorage()
#print form.getlist('p')
#exit()

d = {}

# get a list of nodes from which the database has data
# http://192.168.0.20/node_config.py?p=list_of_nodes
if 'list_of_nodes' in form.getlist('p'):
    site = form.getlist('site')[0]
    '''dbfile = get_dbfile(site)
    if not exists(dbfile):
        # Don't want storage to auto-create an empty database
        # file if it doesn't already exist (such as when being
        # updated by rsync)
        d.update({'list_of_nodes':[]})
    else:
        store = storage_read_only(dbfile=get_dbfile(site))
        nodes = []
        for node_id in get_capabilities(site).keys():
            try:
                time_col = auto_time_col(store,node_id)
                r = store.read_last_N(node_id,time_col)
                if r is not None:
                    nodes.append(node_id)
                #else:
                #    print 'Content-Type: text/plain; charset=utf8'
                #    print
                #    print node_id
            except:
                traceback.print_exc()
        d.update({'list_of_nodes':nodes})'''
    nodes = get_list_of_nodes(site)
    d.update({'list_of_nodes':nodes})

# http://192.168.0.20/node_config.py?p=list_of_variables&id=4
if 'list_of_variables' in form.getlist('p'):
    tags = read_capabilities()[int(form.getlist('id')[0])]['tag']
    d.update({'list_of_variables':tags})

# get the latest sample of all variables (tags/columns) in the database
# http://192.168.0.20/node_config.py?site=poh&p=latest_sample&id=4
if 'latest_sample' in form.getlist('p'):
    site = form.getlist('site')[0]
    node_id = form.getlist('node_id')[0]
    dbfile = get_dbfile(site,node_id=node_id)
    if not exists(dbfile):
        # Don't want storage to auto-create an empty database
        # file if it doesn't already exist (such as when being
        # updated by rsync)
        d.update({'list_of_nodes':[]})
    else:
        store = storage_read_only(dbfile=dbfile)
        time_col = auto_time_col(store,node_id)
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
# http://192.168.0.20/node_config.py?p=units&id=4
if 'units' in form.getlist('p'):
    site = form.getlist('site')[0]
    node_id = form.getlist('node_id')[0]
    d.update({'units':get_unit_map(site,node_id)})

if 'description' in form.getlist('p'):
    site = form.getlist('site')[0]
    node_id = form.getlist('node_id')[0]
    d.update({'description':get_description_map(site,node_id)})

# http://192.168.0.20/node_config.py?p=list_of_disp_vars&id=4
if 'list_of_disp_vars' in form.getlist('p'):
    site = form.getlist('site')[0]
    node_id = form.getlist('node_id')[0]
    r = get_list_of_disp_vars(site,node_id)
    d.update({'list_of_disp_vars':r})

# get name of the node with the given ID
# http://192.168.0.20/node_config.py?p=node_name&id=4
if 'node_name' in form.getlist('p'):
    site = form.getlist('site')[0]
    node_id = form.getlist('node_id')[0]
    d.update({'node_name':get_name(site,node_id)})

# http://192.168.0.20/node_config.py?p=node_note&id=4
if 'node_note' in form.getlist('p'):
    site = form.getlist('site')[0]
    node_id = form.getlist('node_id')[0]
    d.update({'node_note':get_note(site,node_id)})

# http://192.168.0.20/node_config.py?p=node_id
#if 'node_id' in form.getlist('p'):
    #d.update({'node_id':get_node_id()})

jsonstr = json.dumps(d,separators=(',',':'))
#print 'Content-Type: text/plain; charset=utf8'
print 'Content-Type: application/json; charset=utf8'
print
print jsonstr

