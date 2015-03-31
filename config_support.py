#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. March 2015
import re
from os.path import join,exists,getmtime,dirname
from ConfigParser import RawConfigParser
from matplotlib import colors


def PRINT(s):
    pass
    #print(s)


def read_config(filename='node_config.ini',pattern='.*'):
    if exists(filename):
        parser = RawConfigParser(allow_no_value=True)
        parser.read(filename)

        config = {}
        for s in parser.sections():
            if re.match(pattern,s):
                config[s] = dict(parser.items(s))
        return config
    else:
        raise IOError('read_config(): {} not found'.format(filename));


# for caching the capabilities of the nodes
# for efficiency (don't want to read the config file for each message received)
def read_capability(config=None):
    if config is None:
        config = join(dirname(__file__),'node_config.ini')
    node_config = read_config(config,pattern='^node_\d{3}$')
    nodes = {}

    for node in node_config.keys():
        #PRINT(node)
        node_id = int(node[5:])
        name = node_config[node]['name']
        dbtag = [c.strip() for c in node_config[node]['dbtag'].split(',')]
        dbtype = [c.strip() for c in node_config[node]['dbtype'].split(',')]
        dbunit = [c.strip() for c in node_config[node]['dbunit'].split(',')]
        msgfield = None
        try:
            msgfield = [c.strip() for c in node_config[node]['msgfield'].split(',')]
        except Exception as e:
            PRINT('read_capability(): msgfield not found (optional for node).')
        convf = None
        try:
            convf = [eval(v) for v in node_config[node]['convf'].split(',')]
        except Exception as e:
            PRINT('read_capability(): convf not found (optional for node).')

        assert len(dbtag) == len(dbtype),\
               'dbtag and dbtype should have the same length'
#        assert len(msgfield) == len(convf),\
#               'msgfield and convf should have the same length'

        nodes[node_id] = {'name':name,
                          'dbtag':dbtag,
                          'dbtype':dbtype,
                          'dbunit':dbunit,
                          'msgfield':msgfield,
                          'convf':convf}
    return nodes


def read_disp_config(config=None):
    if config is None:
        config = join(dirname(__file__),'display_config.ini')
    # could have used JSON...
    display_config = read_config(config,pattern='^node_\d{3}$')
    node_list = sorted(display_config.keys())

    config = {}
    for node in node_list:
        node_id = int(node[5:8])
        
        config[node_id] = {}
        config[node_id]['variable'] = [v.strip() for v in display_config[node]['variable'].split(',')]
        try:
            config[node_id]['plot_dir'] = display_config[node]['plot_dir']
        except KeyError:
            config[node_id]['plot_dir'] = join('./www',node)
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
        config[node_id]['linecolor'] = [C[c] for c in linecolors]
    return config
        

# clumsy...
def get_unit(node_id,tags):
    if type(tags) is not list:
        tags = [tags]
    tmp = read_capability()
    dbtag = tmp[node_id]['dbtag']
    dbunit = tmp[node_id]['dbunit']
    tag_to_unit_dict = dict(zip(dbtag,dbunit))
    units = [tag_to_unit_dict[v] for v in tags]
    if len(units) == 1:
        units = units[0]
    return units


# extremely clumsy...
def get_color(node_id,tags):
    if type(tags) is not list:
        tags = [tags]
    tmp = read_disp_config()
    variable = tmp[node_id]['variable']
    linecolor = tmp[node_id]['linecolor']
    tmp = dict(zip(variable,linecolor))
    colors = [tmp[v] for v in tags]
    if len(colors) == 1:
        colors = colors[0]
    return colors

