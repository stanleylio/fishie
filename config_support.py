#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. March 2015
import re
from os.path import join,exists,getmtime,dirname
from ConfigParser import RawConfigParser
from matplotlib import colors
# do NOT remove this if there is lambda function defined in the config file!
# or else Python would throw some really cryptic error messages...
# because who knows when and where that anonymous function is going to be called.
from datetime import datetime
# should have used JSON to avoid all this mess. comes with field names and
# data type. gets rid of convf nicely. TODO


def PRINT(s):
    pass
    #print(s)


node_config_file = 'node_config.ini'
if not exists(node_config_file):
    node_config_file = '../node_config.ini'
if not exists(node_config_file):
    node_config_file = join(dirname(__file__),'node_config.ini')
assert exists(node_config_file)

def read_config(pattern='.*',configini=None):
    parser = RawConfigParser(allow_no_value=True)
    if configini is None:
        if not exists(node_config_file):
            raise IOError('read_config(): {} not found'.format(filename))
        parser.read(node_config_file)
    else:
        parser.read(configini)

    tmp = {}
    for s in parser.sections():
        if re.match(pattern,s):
            tmp[s] = dict(parser.items(s))
    return tmp


# these look clumsy and redundant, but only because ini is used.
# the next iteration should probably use py or at least json, even xml.
# data structure that has hierarchy.

def is_node():
    tmp = read_config()
    return 'node' in tmp.keys() and 'base' not in tmp.keys()

def is_base():
    # for now. there could be more than two types of nodes in the future...
    return not is_node()

def get_node_id():
    assert is_node()
    return int(read_config()['node']['id'])

def get_broadcast_port():
    assert is_node()
    return read_config()['node']['broadcast_port']

def get_broadcast_baud():
    assert is_node()
    return read_config()['node']['broadcast_baud']

# bad name. more like "idle time between consecutive sampling periods"
def get_interval():
    assert is_node()
    return int(read_config()['node']['wait'])

def get_optode_port():
    assert is_node()
    try:
        tmp = read_config()['node']['optode_port']
        if exists(tmp):
            return tmp
    except KeyError:
        pass
    return None
    
def get_msgfield(node_id=None):
    assert node_id is not None or is_node()
    if node_id is None:
        node_id = get_node_id()
    node_tag = 'node_{:03d}'.format(node_id)
    return [s.strip() for s in read_config()[node_tag]['msgfield'].split(',')]

def get_name(node_id=None):
    assert node_id is not None or is_node()
    if node_id is None:
        node_id = get_node_id()
    node_tag = 'node_{:03d}'.format(node_id)
    return read_config()[node_tag]['name']

def get_note(node_id=None):
    assert node_id is not None or is_node()
    if node_id is None:
        node_id = get_node_id()
    node_tag = 'node_{:03d}'.format(node_id)
    try:
        return read_config()[node_tag]['note']
    except KeyError:
        return None

def get_db(name,node_id=None):
    assert node_id is not None or is_node()
    if node_id is None:
        node_id = get_node_id()
    node_tag = 'node_{:03d}'.format(node_id)
    return [c.strip() for c in read_config()[node_tag][name].split(',')]

def get_dbtag(node_id=None):
    return get_db('dbtag',node_id=node_id)

def get_dbtype(node_id=None):
    return get_db('dbtype',node_id=node_id)

def get_dbunit(node_id=None):
    return get_db('dbunit',node_id=node_id)

def get_description(node_id=None):
    assert node_id is not None or is_node()
    if node_id is None:
        node_id = get_node_id()
    node_tag = 'node_{:03d}'.format(node_id)
    try:
        return [c.strip() for c in read_config()[node_tag]['description'].split(',')]
    except KeyError:
        return None

# this one is meaningless for a sensor node. I AM the sensor node, what "list of node"?
def get_list_of_node():
    #assert is_base()
    return [int(k[5:8]) for k in read_config(pattern='^node_\d{3}$').keys()]

def get_convf(node_id):
    assert is_base()
    node_tag = 'node_{:03d}'.format(node_id)
    return [eval(c.strip()) for c in read_config()[node_tag]['convf'].split(',')]

def read_capability():
    capability = {}
    for node_id in get_list_of_node():
        name = get_name(node_id=node_id)
        dbtag = get_dbtag(node_id=node_id)
        dbtype = get_dbtype(node_id=node_id)
        dbunit = get_dbunit(node_id=node_id)
        msgfield = None
        try:
            msgfield = get_msgfield(node_id=node_id)
        except Exception as e:
            PRINT('read_capability(): msgfield not found (optional for node).')
        convf = None
        try:
            convf = get_convf(node_id=node_id)
        except Exception as e:
            PRINT('read_capability(): convf not found (optional for node).')

        assert len(dbtag) == len(dbtype),\
               'dbtag and dbtype should have the same length'
        assert convf is None or len(msgfield) == len(convf),\
               'msgfield and convf should have the same length'

        capability[node_id] = {'name':name,
                          'dbtag':dbtag,
                          'dbtype':dbtype,
                          'dbunit':dbunit,
                          'msgfield':msgfield,
                          'convf':convf}
    return capability

def read_disp_config(config=None):
    if config is None:
        config = join(dirname(__file__),'display_config.ini')
    if not exists(config):
        raise IOError('read_disp_config(): {} not found'.format(filename))
    
    display_config = read_config(configini=config)
    node_list = sorted(display_config.keys())

    config = {}
    for node in node_list:
        node_id = int(node[5:8])
        
        config[node_id] = {}
        config[node_id]['variable'] = [v.strip() for v in display_config[node]['variable'].split(',')]
        try:
            config[node_id]['html_dir'] = display_config[node]['html_dir']
        except KeyError:
            config[node_id]['html_dir'] = join('./www',node)
        try:
            config[node_id]['plot_dir'] = display_config[node]['plot_dir']
        except KeyError:
            config[node_id]['plot_dir'] = join('./www/node_{:03d}'.format(node_id),node)
        try:
            config[node_id]['time_col'] = display_config[node]['time_col']
        except KeyError:
            config[node_id]['time_col'] = 'Timestamp'
        try:
            config[node_id]['linestyle'] = display_config[node]['linestyle'].split(',')
        except KeyError:
            config[node_id]['linestyle'] = ['-' for v in config[node_id]['variable']]
        try:
            linecolors = display_config[node]['linecolor'].split(',')
        except KeyError:
            linecolors = ['b' for v in config[node_id]['variable']]
        C = {k:colors.cnames[k] for k in colors.cnames}
        C.update(colors.ColorConverter.colors)
        config[node_id]['linecolor'] = [C[c.lower()] for c in linecolors]
    return config
        

# given dbtag, return dbunit
# input can be a list of tag or just one tag
# clumsy... inefficient...
# also should keep this simple: accept only one tag, not list of tags.
# use list comprehension for the list case.
def get_unit(node_id,tags):
    islist = type(tags) is list
    if not islist:
        tags = [tags]
    dbtag = get_dbtag(node_id=node_id)
    dbunit = get_dbunit(node_id=node_id)
    tmp = dict(zip(dbtag,dbunit))
    units = [tmp[v] for v in tags]
    if not islist:
        units = units[0]
    return units

def tag2description(node_id,tag):
    tags = get_dbtag(node_id=node_id)
    desc = get_description(node_id=node_id)
    return dict(zip(tags,desc))[tag]

# extremely clumsy...
def get_color(node_id,tags):
    islist = type(tags) is list
    if not islist:
        tags = [tags]
    tmp = read_disp_config()
    variable = tmp[node_id]['variable']
    linecolor = tmp[node_id]['linecolor']
    tmp = dict(zip(variable,linecolor))
    colors = [tmp[v] for v in tags]
    if not islist:
        colors = colors[0]
    return colors


if '__main__' == __name__:
    print is_node()
    print is_base()

    print tag2description(4,'Pressure_MS5803')

    # node only
    try:
        print get_node_id()
        print get_broadcast_port()
        print get_broadcast_baud()
        print get_interval()
        print get_msgfield()
        print get_name()
        print get_dbtag()
        print get_dbtype()
        print get_dbunit()
    except:
        pass

    # base station only
    try:
        print get_convf()
        print get_list_of_node()
    except:
        pass


