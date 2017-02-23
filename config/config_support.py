#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. August 2015
#from __future__ import absolute_import
import re,socket,traceback#,imp
from importlib import import_module
from os import listdir
from os.path import join,exists,dirname,realpath,basename,splitext


def config_as_dict():
    from os import listdir
    from os.path import dirname,abspath,samefile,join,isfile

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

#def get_node_tag():
    #return socket.gethostname()

#def is_node():
    #return re.match('^node.+',get_node_tag())

#def is_base():
    #return re.match('^base.+',get_node_tag())

def get_site(node):
    """Meant to be called by the base stations / nodes to find out which site it belongs"""
    C = config_as_dict()
    for site in C:
        if node in C[site]:
            return site

def import_node_config(site=None,node=None):
    """Meant to be called by the base stations / nodes to get its own config file"""
    if node is None:
        from socket import gethostname
        node = gethostname()
    if site is None:
        site = get_site(node)
    node = node.replace('-','_')
    return import_module('node.config.{site}.{node}'.\
                         format(site=site,node=node))

def get_list_of_nodes(site):
    c = config_as_dict()
    L = c.get(site,[])
    L = filter(lambda x: x.startswith('node-'),L)
    return sorted(L)

def get_list_of_variables(site,node):   # TODO: remove 'site'
    node = import_node_config(site,node)
    return [c['dbtag'] for c in node.conf]

def get_type(site,node):                # TODO: remove 'site'
    node = import_node_config(site,node)
    return [c['dbtype'] for c in node.conf]

# should be OBSOLETE by now
# really this should be "get data source" - it doesn't matter it's a csv, an sqlite or mysql db.
#def get_dbfile(site,node):
#    node = import_node_config(site,node)
#    return node.data_source

def get_public_key(site,device):
    node = import_node_config(site,device)
    return node.public_key

def get_schema(site):
    return {node:zip(get_list_of_variables(site,node),get_type(site,node)) for node in get_list_of_nodes(site)}


# STUFF FOR WEB PRESENTATION ONLY
def get_attr(node,attr):
    site = get_site(node)
    m = import_node_config(site,node.replace('-','_'))
    return getattr(m,attr,None)

'''def get_name(site,node):
    node = node.replace('-','_')
    return import_node_config(site,node).name

def get_note(site,node):
    node = node.replace('-','_')
    return import_node_config(site,node).note

def get_location(site,node):
    node = node.replace('-','_')
    return import_node_config(site,node).location

def get_google_earth_link(site,node):
    node = node.replace('-','_')
    try:
        return import_node_config(site,node).google_earth_link
    except AttributeError:
        return '#'
'''

def get_unit_map(node):
    node = import_node_config(node=node)
    return {c['dbtag']:c.get('unit',None) for c in node.conf}

def get_unit(node,var):
    return get_unit_map(node)[var]

def get_description_map(node):
    node = import_node_config(node=node)
    return {c['dbtag']:c.get('description','') for c in node.conf}

def get_description(node,var):
    return get_description_map(node)[var]

def get_list_of_disp_vars(node):
    """Get the list of variables to display."""
    node = import_node_config(node=node)
    return [c['dbtag'] for c in node.conf if c.get('plot',True)]

def get_plot_range(node):
    site = get_site(node)
    try:
        return import_node_config(site,node).plot_range
    except AttributeError:
        return 30*24    # default: ~30 days


class Range(object):
    # there goes the language-agnostic age... all these for being able to:
    # if reading in range:
    # if you want to get fancy, distinguish (,) from [,], or even (,] and [,)
    def __init__(self,lb=float('-inf'),ub=float('inf')):
        assert lb <= ub
        self._lb = lb
        self._ub = ub

    def to_tuple(self):
        return (self._lb,self._ub)

    def __getitem__(self,key):
        if 'lb' == key:
            return self._lb
        if 'ub' == key:
            return self._ub
        return None
        
    def __contains__(self,item):
        # >= instead of > because it's kinda strange to have
        # 10 in Range(1,10) evaluate to False
        return item >= self._lb and item <= self._ub

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.to_tuple())

def get_range(site,node_id,variable):
    node = import_node_config(site,node_id)
    for c in node.conf:
        if c['dbtag'] == variable:
            try:
                return c['range']
            except:
                return None

def is_in_range(site,node,variable,reading):
    try:
        return reading in get_range(site,node,variable)
    except:
        #traceback.print_exc()
        return True


if '__main__' == __name__:

    #print config_as_dict()
    print get_list_of_nodes('poh')

    '''site = 'poh'
    print get_list_of_nodes(site)
    print 
    print is_in_range('poh','node-003','P_5803',100)
    #print
    #print Range(100,200).__dict__
    #print Range(100,200).keys()        # enough of the acrobatics.'''
    
