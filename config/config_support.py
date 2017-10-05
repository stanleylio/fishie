#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. August 2015
#from __future__ import absolute_import
import re,socket,traceback#,imp
from importlib import import_module
from os import listdir
from os.path import join,exists,dirname,realpath,basename,splitext,abspath,isfile


def config_as_dict():
    def dironly(p):
        return [f for f in listdir(p) if not isfile(join(p,f))]

    def fileonly(p):
        return [f for f in listdir(p) if isfile(join(p,f))]

    cdir = dirname(abspath(__file__))
    sites = dironly(cdir)

    config = {}
    for site in sites:
        F = fileonly(join(cdir,site))
        F = filter(lambda x: x.endswith('.py'),F)
        F = filter(lambda x: not x.startswith('__init__'),F)
        F = [f.replace('.py','') for f in F]
        F = [f.replace('_','-') for f in F]
        if len(F):
            config[site] = sorted(F)
    return config

def get_site(node):
    """Meant to be called by the base stations / nodes to find out which site it belongs"""
    C = config_as_dict()
    for site in C:
        if node in C[site]:
            return site

def import_node_config(node=None):
    """Meant to be called by the base stations / nodes to get its own config file"""
    if node is None:
        from socket import gethostname
        node = gethostname()
    site = get_site(node)
    node = node.replace('-','_')
    return import_module('node.config.{site}.{node}'.\
                         format(site=site,node=node))

def get_list_of_devices(site):
    return sorted(config_as_dict().get(site,[]))

def get_list_of_nodes(site):
    #L = config_as_dict().get(site,[])
    #L = filter(lambda x: x.startswith('node-'),L)
    #return sorted(L)
    return filter(lambda x: x.startswith('node-'),get_list_of_devices(site))

def get_list_of_variables(node):
    node = import_node_config(node)
    conf = getattr(node,'conf',None)
    if conf is None:
        return []
    return [c['dbtag'] for c in node.conf]

def get_type(site,node):
    node = import_node_config(node)
    return [c.get('dbtype','DOUBLE') for c in node.conf]

#def get_schema(site):
#    return {node:zip(get_list_of_variables(node),get_type(site,node)) for node in get_list_of_nodes(site)}


# STUFF FOR WEB
def get_attr(node,attr,default=None):
    m = import_node_config(node)
    return getattr(m,attr,default)

def get_public_key(node):
    return get_attr(node,'public_key',default=None)

def get_unit_map(node):
    node = import_node_config(node=node)
    return {c['dbtag']:c.get('unit',None) for c in node.conf}

def get_unit(node,var):
    return get_unit_map(node).get(var,None)

def get_description_map(node):
    node = import_node_config(node=node)
    return {c['dbtag']:c.get('description','') for c in node.conf}

def get_description(node,var):
    return get_description_map(node).get(var,'')

def get_list_of_disp_vars(node):
    """Get the list of variables to display."""
    node = import_node_config(node=node)
    conf = getattr(node,'conf',[])
    return [c['dbtag'] for c in conf if c.get('plot',True)]

def get_plot_range(node):
#    try:
#        return import_node_config(node).plot_range
#    except AttributeError:
#        return 30*24    # default: ~30 days
    return get_attr(node,'plot_range',default=30*24)

def get_range(node,variable):
    node = import_node_config(node=node)
    conf = getattr(node,'conf',[])
    for c in conf:
        if c['dbtag'] == variable:
            return [c.get('lb',float('-inf')),
                    c.get('ub',float('inf'))]
    return None

def is_in_range(site,node,variable,reading):
    try:
        r = get_range(site,node,variable)
        return reading >= min(r) and reading <= max(r)
    except:
        #traceback.print_exc()
        return True

def get_interval(node,variable):
    node = import_node_config(node=node)
    for c in node.conf:
        if c['dbtag'] == variable:
            return c.get('interval',30*60)
    return None


if '__main__' == __name__:
    #print config_as_dict()
    print get_list_of_nodes('poh')
