#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. August 2015
import re,socket
from os import listdir
from os.path import join,exists,dirname,realpath
from ConfigParser import RawConfigParser


def PRINT(s):
    pass
    #print(s)


node_tag = socket.gethostname()
PRINT(node_tag)

def is_node():
    return re.match('^node-\d{3}$',node_tag)

def is_base():
    return re.match('^base-\d{3}$',node_tag)

# node and base station are not the only two types of device that
# need this script - for example, plotting on laptop
if not (is_node() or is_base()):
    PRINT('config_support.py: Warning: Cannot identify this node.')

node_id = None
if is_node():
    node_id = int(node_tag[5:8])

config_file = join(dirname(__file__),node_tag + '.py')
if not exists(config_file):
    PRINT('config_support.py: Warning: {} not found'.format(config_file))


def get_list_of_nodes():
    #return sorted([int(l[5:8]) for l in listdir(dirname(realpath(__file__))) if re.match('^node-\d{3}\.ini$',l)])
    return sorted([int(l[5:8]) for l in listdir(dirname(realpath(__file__))) if re.match('^node_\d{3}\.py$',l)])

def get_tag(i):
    exec('import node_{:03d} as node'.format(i))
    return [c['dbtag'] for c in node.conf]

def get_type(i):
    exec('import node_{:03d} as node'.format(i))
    return [c['dbtype'] for c in node.conf]

def get_unit(i):
    exec('import node_{:03d} as node'.format(i))
    return [c['unit'] for c in node.conf]

def read_capabilities():
    capabilities = {}
    for node_id in get_list_of_nodes():
        dbtag = get_tag(node_id)
        dbtype = get_type(node_id)
        assert len(dbtag) == len(dbtype),\
               'each tag defined should have a corresponding type and vice versa'

        capabilities[node_id] = {
            'tag':dbtag,
            'type':dbtype}
    assert len(capabilities.keys()) > 0
    return capabilities


# BASE-ONLY
pass


# NODE-ONLY
'''def get_flntu_port():
    assert is_node()
    try:
        tmp = read_config()['node']['flntu_port']
        if exists(tmp):
            return tmp
    except KeyError:
        return None'''

def get_node_id():
    assert is_node()
    return node_id


# STUFF FOR THE WEB PAGE ONLY
def get_name(node_id=None):
    try:
        # These really are two different tasks:
        # one asks what the name of THIS node is
        # one asks what the name of the node with the given ID is
        # not sure I should put them both here.
        if node_id is None:
            if is_node():
                return read_config()['node']['name']
            elif is_base():
                return read_config()['base']['name']
        else:
            node_tag = 'node-{:03d}'.format(node_id)
            configfile = join(dirname(__file__),node_tag + '.ini')
            assert exists(configfile),'get_name(): something something missing...'
            return read_ini(configfile)['node']['name']
    except KeyError:
        return None

def get_note(node_id=None):
    # same as get_name, refactor them? TODO
    try:
        if node_id is None:
            if is_node():
                return read_config()['node']['note']
            elif is_base():
                return read_config()['base']['note']
        else:
            node_tag = 'node-{:03d}'.format(node_id)
            configfile = join(dirname(__file__),node_tag + '.ini')
            assert exists(configfile),'get_note(): something something missing...'
            return read_ini(configfile)['node']['note']
    except KeyError:
        return None

def get_description(node_id=None):
    return get_db('description',node_id=node_id)

# get the list of variables to display
# TODO: merge this with get_db()?
def get_list_of_disp_vars(node_id=None):
    assert node_id is not None or is_node()
    if node_id is None:
        node_id = get_node_id()
    node_tag = 'node-{:03d}'.format(node_id)
    configfile = join(dirname(__file__),node_tag + '.ini')
    assert exists(configfile),'get_db(): something something missing...'
    return [c.strip() for c in read_ini(configfile)['display']['variable'].split(',')]


if '__main__' == __name__:
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
    
