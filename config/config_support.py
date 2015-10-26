#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. August 2015
import re,socket,importlib
from os import listdir
from os.path import join,exists,dirname,realpath
from ConfigParser import RawConfigParser

def PRINT(s):
    print(s)
    #pass

def get_node_tag():
    return socket.gethostname()

def is_node():
    return re.match('^node-\d{3}$',get_node_tag())

def is_base():
    return re.match('^base-\d{3}$',get_node_tag())

# node and base station are not the only two types of device that
# need this script - for example, plotting on laptop
if not (is_node() or is_base()):
    PRINT('config_support.py: Warning: Cannot identify the current device: ' + get_node_tag())

def get_list_of_nodes():
    return sorted([int(l[5:8]) for l in listdir(dirname(realpath(__file__))) if re.match('^node_\d{3}\.py$',l)])

def get_tag(node_id):
    node = importlib.import_module('config.node_{:03d}'.format(node_id))
    return [c['dbtag'] for c in node.conf]

def get_type(node_id):
    node = importlib.import_module('config.node_{:03d}'.format(node_id))
    return [c['dbtype'] for c in node.conf]

#def get_unit(node_id):
#    node = importlib.import_module('config.node_{:03d}'.format(node_id))
#    return [c['unit'] for c in node.conf]

def read_capabilities():
    capabilities = {}
    for node_id in get_list_of_nodes():
        dbtag = get_tag(node_id)
        dbtype = get_type(node_id)

        capabilities[node_id] = {
            'tag':dbtag,
            'type':dbtype}
    assert len(capabilities.keys()) > 0
    return capabilities


# BASE-ONLY
pass


# NODE-ONLY
def get_node_id():
    assert is_node()
    return int(get_node_tag()[5:8])


# STUFF FOR THE WEB PAGE ONLY
def get_name(node_id):
    node = importlib.import_module('config.node_{:03d}'.format(node_id))
    return node.name

def get_note(node_id):
    node = importlib.import_module('config.node_{:03d}'.format(node_id))
    return node.note

def get_unit_map(node_id):
    node = importlib.import_module('.node_{:03d}'.format(node_id),'config')
    return {c['dbtag']:c['unit'] for c in node.conf}

#def get_description(node_id,tag):
#    node = importlib.import_module('config.node_{:03d}'.format(node_id))
#    return [c for c in node.conf if c['dbtag'] == tag][0]['description']

def get_description_map(node_id):
    node = importlib.import_module('.node_{:03d}'.format(node_id),'config')
    return {c['dbtag']:c['description'] for c in node.conf}

# get the list of variables to display
# TODO: merge this with get_db()?
def get_list_of_disp_vars(node_id=None):
    assert node_id is not None or is_node()
    if node_id is None:
        node_id = get_node_id()
    node = importlib.import_module('config.node_{:03d}'.format(node_id))
    return [c['dbtag'] for c in node.conf if c['plot']]


if '__main__' == __name__:

    import sys
    print sys.path
    
    print get_description_map(4)
    exit()

    print get_name()
    exit()
    print 'is_node(): ',bool(is_node())
    print 'is_base(): ',bool(is_base())

    print 'get_xbee_port(): ',get_xbee_port()
    print 'get_xbee_baud(): ',get_xbee_baud()

    if is_node():
        print 'get_node_id(): ',get_node_id()
        print 'get_interval(): ',get_interval()

    print
    print

    print read_capabilities()
    
