#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,pytz,re
sys.path.append('storage')
from jinja2 import Template
from os.path import getmtime,dirname,join
from storage import storage
from datetime import datetime
from parse_support import read_capability
from ConfigParser import RawConfigParser,NoSectionError


def gen_page(node_id,template_path,output_path):
    with open(template_path,'r') as f:
        template = Template(f.read())

    node_capability = read_capability()
    dbtag = node_capability[node_id]['dbtag']
    dbunit = node_capability[node_id]['dbunit']
    units = dict(zip(dbtag,dbunit))

    parser = RawConfigParser()
    parser.read(join(dirname(__file__),'display_config.ini'))
    variables = parser.get('node_{:03d}'.format(node_id),'variable').split(',')
    time_col = parser.get('node_{:03d}'.format(node_id),'time_col')

    # retrieve all the variables, plus Timestamp (or ReceptionTime, depending on the node)
    # all variables have associated ReceptionTime, but don't always have Timestamp
    store = storage()
    col_name = [time_col]
    col_name.extend(variables)
    tmp = store.read_latest(node_id,col_name,time_col=time_col)
    ts = tmp[time_col][0]
    values = ['{:.2f}'.format(tmp[v][0]) for v in variables]
    units = [units[v] for v in variables]
    table = zip(variables,values,units)
    
    img_src = ['./node_{:03d}/{}.png'.format(node_id,var) for var in variables]
    img_header = variables
    img_alt = variables
    plots = zip(img_header,img_src,img_alt)

    ts = ts.replace(tzinfo=pytz.timezone('UTC'))
    #ts = ts.replace(tzinfo=pytz.timezone('America/Los_Angeles'))

    node_id = 'Node #{}'.format(node_id)
    title_str = 'Environmental Monitoring'
    timeelement = '<time class="timeago" datetime="{}">ago</time>'.format(ts.isoformat())
    status_str = 'Last reading in plot sampled at {} UTC ({})'.format(ts.strftime('%Y-%m-%d %H:%M:%S'),timeelement)
    #status_str = 'Last reading in plot sampled at {} PST ({})'.format(ts.strftime('%Y-%m-%d %H:%M:%S'),timeelement)
    setting_str = 'Median filter: {}'.format('<b>OFF</b>')
    body_text = '<a href=./memory_usage.png>Memory Usage</a>'

    tmp = template.render({'title_str':title_str,
                           'node_id':node_id,
                           'status_str':status_str,
                           'setting_str':setting_str,
                           'body_text':body_text},
                          TABLE=table,PLOTS=plots)

    #print tmp
    
    with open(output_path,'w') as f:
        f.write(tmp)


if '__main__' == __name__:
    # remember the .css and .js too
    template_path = './template/node_template.html'

    parser = RawConfigParser()
    parser.read(join(dirname(__file__),'display_config.ini'))
    for s in parser.sections():
        if re.match('^node_\d{3}$',s):
            node_id = int(s[5:8])
            output_path = parser.get(s,'html_dir')
            
            print('Generating webpage for node {}...'.format(node_id))
            gen_page(node_id,template_path,output_path)
    
