#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. August 2015
#from __future__ import absolute_import
import re,socket,traceback,imp#,importlib
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

def import_node_config(site,node):
    """Import the appropriate config file for the given (site,node)"""
    #return importlib.import_module('config.' + site + '.' + node.replace('-','_'))
    tmp = join(dirname(realpath(__file__)),site,node.replace('-','_') + '.py')
    return imp.load_source('node',tmp)

def get_list_of_nodes(site):
    d = join(dirname(realpath(__file__)),site)
    L = listdir(d)
    L = [l for l in L if re.match('^node_\d{3}\.py$',l)]
    L = [basename(splitext(l)[0]) for l in L]
    L = [l.replace('_','-') for l in L]
    return sorted(L)

def get_tag(site,node):
    node = import_node_config(site,node)
    return [c['dbtag'] for c in node.conf]

def get_type(site,node):
    node = import_node_config(site,node)
    return [c['dbtype'] for c in node.conf]


# TODO: replace get_capabilities() with this...
# or even better, just return an SQL string.
# in either case, since I know there are only "column name" and "data type", I can
# put them in (tag,type) without the dict's "tags" "types" keys.
def get_schema(site):
    return {node:zip(get_tag(site,node),get_type(site,node)) for node in get_list_of_nodes(site)}

def get_capabilities(site):
    capabilities = {}
    for node in get_list_of_nodes(site):
        dbtag = get_tag(site,node)
        dbtype = get_type(site,node)

        capabilities[node] = {
            'tag':dbtag,
            'type':dbtype}
    assert len(capabilities.keys()) > 0
    return capabilities


# STUFF FOR PRESENTATION ONLY
def get_name(site,node):
    return import_node_config(site,node).name

def get_note(site,node):
    return import_node_config(site,node).note

def get_location(site,node):
    return import_node_config(site,node).location

def get_unit_map(site,node):
    node = import_node_config(site,node)
    return {c['dbtag']:c['unit'] for c in node.conf}

def get_description_map(site,node):
    node = import_node_config(site,node)
    return {c['dbtag']:c['description'] for c in node.conf}

# if it really is "node", then it shouldn't accept "node_003"
# but instead ask for "node-003". Bug + Bug = working... TODO
def get_list_of_disp_vars(site,node):
    """Get the list of variables to display."""
    node = import_node_config(site,node)
    return [c['dbtag'] for c in node.conf if c['plot']]

class Range(object):
    # there goes the language-agnostic age... all these for being able to:
    # if reading in range:
    # if you want to get fancy, distinguish (,) from [,], or even (,] and [,)
    def __init__(self,lb=float('-inf'),ub=float('inf')):
        assert lb <= ub
        self._lb = lb
        self._ub = ub

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
        return str((self._lb,self._ub))

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

    site = 'poh'
    print get_list_of_nodes(site)
    print 
    print get_capabilities(site)
    print
    print is_in_range('poh','node-003','P_5803',100)
    #print
    #print Range(100,200).__dict__
    #print Range(100,200).keys()        # enough of the acrobatics.
    
