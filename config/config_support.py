#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. August 2015
#from __future__ import absolute_import
import re,socket#,importlib
from os import listdir
from os.path import join,exists,dirname,realpath,basename,splitext
from ConfigParser import RawConfigParser


def PRINT(s):
    print(s)
    #pass

def get_node_tag():
    return socket.gethostname()

def is_node():
    return re.match('^node.+',get_node_tag())

def is_base():
    return re.match('^base.+',get_node_tag())

def import_node_config(site,node_id):
    #return importlib.import_module('config.' + site + '.' + node_id.replace('-','_'))
    import imp
    tmp = join(dirname(realpath(__file__)),site,node_id.replace('-','_') + '.py')
    return imp.load_source('node',tmp)

def get_list_of_nodes(site):
    d = join(dirname(realpath(__file__)),site)
    L = listdir(d)
    L = [l for l in L if re.match('^node_\d{3}\.py$',l)]
    L = [basename(splitext(l)[0]) for l in L]
    L = [l.replace('_','-') for l in L]
    return sorted(L)

def get_tag(site,node_id):
    node = import_node_config(site,node_id)
    return [c['dbtag'] for c in node.conf]

def get_type(site,node_id):
    node = import_node_config(site,node_id)
    return [c['dbtype'] for c in node.conf]

def get_capabilities(site):
    capabilities = {}
    for node_id in get_list_of_nodes(site):
        dbtag = get_tag(site,node_id)
        dbtype = get_type(site,node_id)

        capabilities[node_id] = {
            'tag':dbtag,
            'type':dbtype}
    assert len(capabilities.keys()) > 0
    return capabilities


# STUFF FOR THE WEB PAGE ONLY
def get_name(site,node_id):
    return import_node_config(site,node_id).name

def get_note(site,node_id):
    return import_node_config(site,node_id).note

def get_unit_map(site,node_id):
    node = import_node_config(site,node_id)
    return {c['dbtag']:c['unit'] for c in node.conf}

def get_description_map(site,node_id):
    node = import_node_config(site,node_id)
    return {c['dbtag']:c['description'] for c in node.conf}

# get the list of variables to display
def get_list_of_disp_vars(site,node_id):
    node = import_node_config(site,node_id)
    return [c['dbtag'] for c in node.conf if c['plot']]


if '__main__' == __name__:

    site = 'poh'
    print get_list_of_nodes(site)
    print 
    print get_capabilities(site)
    
