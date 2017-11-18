#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. August 2015
#from __future__ import absolute_import
import re,socket,traceback
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

def get_site(device):
    """Look up which site the given device belongs to"""
    C = config_as_dict()
    for site in C:
        if device in C[site]:
            return site

def import_node_config(device=None):
    if device is None:
        from socket import gethostname
        device = gethostname()
    site = get_site(device)
    device = device.replace('-','_')
    return import_module('node.config.{site}.{device}'.\
                         format(site=site,device=device))

def get_list_of_sites():
    return config_as_dict().keys()

def get_list_of_devices(site):
    return sorted(config_as_dict().get(site,[]))

def get_list_of_nodes(site):
    return filter(lambda x: x.startswith('node-'),get_list_of_devices(site))

def get_list_of_variables(node):
    config = import_node_config(node)
    return [c['dbtag'] for c in getattr(config,'conf',[])]

def get_config(parameter_name,node_id,variable_name=None,default=None):
    # note: None could mean 1. the parameter is not defined, or 2. its value IS None
    config = import_node_config(node_id)

    # variable_name not given, so it's a node-wide parameter
    if variable_name is None:
        return getattr(config,parameter_name,default)

    # is it defined for the particular variable?
    for c in getattr(config,'conf',[]):
        if c['dbtag'] == variable_name:
            return c.get(parameter_name,default)
    return default


# STUFF FOR WEB

# I have a feeling I'm going to regret this some day.
#get_public_key = lambda node: get_config('public_key',node)
get_unit = lambda node,var: get_config('unit',node,variable_name=var,default='-')
get_description = lambda node,var: get_config('description',node,variable_name=var,default='')
get_interval = lambda node,variable: get_config('interval',node,variable_name=variable,default=30*60)
get_plot_range = lambda node,var: get_config('plot_range',node,variable_name=var,default=30*24)

# need some work here. time for SQL I'd say...
def get_list_of_disp_vars(device):
    """Get the list of variables to display."""
    device = import_node_config(device=device)
    conf = getattr(device,'conf',[])
    return [c['dbtag'] for c in conf if c.get('plot',True)]

def get_range(node,var):
    lb = get_config('lb',node,variable_name=var,default=float('-inf'))
    ub = get_config('ub',node,variable_name=var,default=float('inf'))
    return [lb,ub]

def is_in_range(site,node,variable,reading):
    try:
        r = get_range(site,node,variable)
        return reading >= min(r) and reading <= max(r)
    except:
        return True


if '__main__' == __name__:
    #print config_as_dict()
    print(get_list_of_nodes('poh'))
