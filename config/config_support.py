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

assert is_node() or is_base(),\
       'config_support.py: Cannot identify this node.'

node_id = None
if is_node():
    node_id = int(node_tag[5:8])

node_config_file = join(dirname(__file__),node_tag + '.ini')
# later, perhaps this won't be true if base stations start to have their
# own config files
assert is_base() or exists(node_config_file)


# given the path to an ini file, return its content as dict of dicts
def read_ini(inifile,pattern='.*'):
    parser = RawConfigParser(allow_no_value=True)
    parser.read(inifile)

    tmp = {}
    for s in parser.sections():
        if re.match(pattern,s):
            tmp[s] = dict(parser.items(s))
    return tmp

def read_config():
    return read_ini(node_config_file)

def get_xbee_port():
    if is_node():
        return read_config()['node']['xbee_port']
    if is_base():
        return read_config()['base']['xbee_port']

def get_xbee_baud():
    if is_node():
        return int(read_config()['node']['xbee_baud'])
    if is_base():
        return int(read_config()['base']['xbee_baud'])

def get_log_dir():
    if is_node():
        return read_config()['node']['log_dir']
    if is_base():
        return read_config()['base']['log_dir']

def get_list_of_nodes():
    return sorted([int(l[5:8]) for l in listdir(dirname(realpath(__file__))) if re.match('^node-\d{3}\.ini$',l)])

def get_db(name,node_id=None):
    assert node_id is not None or is_node()
    if node_id is None:
        node_id = get_node_id()
    node_tag = 'node-{:03d}'.format(node_id)
    configfile = join(dirname(__file__),node_tag + '.ini')
    assert exists(configfile),'get_db(): something something missing...'
    return [c.strip() for c in read_ini(configfile)['database'][name].split(',')]

def get_tag(node_id=None):
    return get_db('tag',node_id=node_id)

def get_type(node_id=None):
    return get_db('type',node_id=node_id)

def get_unit(node_id=None):
    return get_db('unit',node_id=node_id)

def read_capabilities():
    capabilities = {}
    for node_id in get_list_of_nodes():
        dbtag = get_tag(node_id=node_id)
        dbtype = get_type(node_id=node_id)
        dbunit = get_unit(node_id=node_id)
        assert len(dbtag) == len(dbtype),\
               'tag and type should have the same length'
        assert len(dbtag) == len(dbunit),\
               'tag and unit should have the same length'

        capabilities[node_id] = {
            'tag':dbtag,
            'type':dbtype,
            'unit':dbunit}
    assert len(capabilities.keys()) > 0
    return capabilities


# BASE-ONLY
pass


# NODE-ONLY
def get_node_id():
    assert is_node()
    return int(read_config()['node']['id'])

# bad name. more like "idle time between consecutive sampling periods"
def get_interval():
    assert is_node()
    return int(read_config()['node']['wait'])

# only make sense for those that have optodes...
# should not put them here.
def get_optode_port():
    assert is_node()
    try:
        tmp = read_config()['node']['optode_port']
        if exists(tmp):
            return tmp
    except KeyError:
        return None

def get_flntu_port():
    assert is_node()
    try:
        tmp = read_config()['node']['flntu_port']
        if exists(tmp):
            return tmp
    except KeyError:
        return None

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

    print read_config()
    print 'get_xbee_port(): ',get_xbee_port()
    print 'get_xbee_baud(): ',get_xbee_baud()

    if is_node():
        print 'get_node_id(): ',get_node_id()
        print 'get_interval(): ',get_interval()

    print
    print

    print read_capabilities()
    
