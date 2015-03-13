#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,pytz
sys.path.append('storage')
from jinja2 import Template
from os.path import getmtime,dirname,join,isfile,isdir
from storage import storage
from datetime import datetime,timedelta
from config_support import read_config


def PRINT(s):
    #pass
    print(s)

def gen_front_page(template_path,output_dir):
    assert isfile(template_path),'gen_front_page(): template_path should point to a file'
    assert isdir(output_dir),'gen_front_page(): output_dir should be a directory'
    
    display_config = read_config('display_config.ini',pattern='^node_\d{3}$')
    node_config = read_config('node_config.ini')

    node_list = [k for k in sorted(display_config.keys())]
    node_ids = [int(k[5:8]) for k in node_list]
    node_names = [node_config[k]['name'] for k in node_list]
    #html_list = [display_config[k]['html_dir'] for k in node_list]
    #links = [join(k[0],'{}.html'.format(k[1])) for k in zip(html_list,node_list)]
    links = ['{}.html'.format(k) for k in node_list]
    disp_str = ['Node #{}, {}'.format(k[0],k[1]) for k in zip(node_ids,node_names)]

    with open(template_path,'r') as f:
        template = Template(f.read())
    tmp = template.render(NODE_PAGES=zip(links,disp_str))
    with open(join(output_dir,'index.html'),'w') as f:
        f.write(tmp)


def gen_node_page(node_id,page_template,error_template,output_dir):
    # read the dbtag:dbunit mapping
    tmp = read_config('node_config.ini',pattern='^node_\d{3}$') # can be more specific here.
    tmp = tmp['node_{:03d}'.format(node_id)]
    node_name = tmp['name']
    dbtag = tmp['dbtag'].split(',')
    dbunit = tmp['dbunit'].split(',')
    units = dict(zip(dbtag,dbunit))

    output = join(output_dir,'node_{:03d}.html'.format(node_id))
    PRINT('Output: ' + output)

    # decide the set of variables to tabulate
    tmp = read_config('display_config.ini',pattern='^node_\d{3}$')
    tmp = tmp['node_{:03d}'.format(node_id)]
    variables = []
    try:
        variables = tmp['variable'].split(',')
    except KeyError:
        PRINT('gen_node_page(): no variable to tabulate')
    time_col = 'Timestamp'
    try:
        time_col = tmp['time_col']
    except KeyError:
        PRINT('gen_node_page(): warning: time_col not specified. Default to ' + time_col)

    if len(variables) <= 0:
        PRINT('gen_node_page(): no variable to tabulate and plot. ABORT')
        with open(error_template,'r') as f:
            template = Template(f.read())
        tmp = template.render({'error_message':'No variable specified in display_config.ini for node_{:03d}'.format(node_id)})
        with open(output,'w') as f:
            f.write(tmp)
        return

    # Retrieve the latest readings, plus Timestamp/ReceptionTime
    # NOTE: On the base station, all database records have associated ReceptionTime but
    # don't always have Timestamp (reported by sensor nodes); on nodes they may have neither.
    store = storage()
    try:
        tmp = store.read_latest(node_id,time_col=time_col)
    except Exception as e:
        PRINT('gen_node_page(): error retrieving latest readings, ABORT')
        PRINT(e)
        with open(error_template,'r') as f:
            template = Template(f.read())
        tmp = template.render({'error_message':'Error retrieving latest readings from database.'})
        with open(output,'w') as f:
            f.write(tmp)
        return

    if len(tmp) <= 0:
        err_msg = 'Database contains no record for node_{:03d}.'.format(node_id)
        PRINT('gen_node_page(): {} ABORT'.format(err_msg))
        with open(error_template,'r') as f:
            template = Template(f.read())
        tmp = template.render({'error_message':err_msg})
        with open(output,'w') as f:
            f.write(tmp)
        return
        
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

    node_id_str = 'Node #{} ({})'.format(node_id,node_name)
    title_str = node_id_str
    timeelement = '<time class="timeago" datetime="{}">ago</time>'.format(ts.isoformat())
    status_str = 'Last reading in plot sampled at {} UTC ({})'.format(ts.strftime('%Y-%m-%d %H:%M:%S'),timeelement)
    #status_str = 'Last reading in plot sampled at {} PST ({})'.format(ts.strftime('%Y-%m-%d %H:%M:%S'),timeelement)
    setting_str = 'Median filter: {}'.format('<b>OFF</b>')
# TODO: every time you use a magic number god kills a kitten.
    tmp = store.read_time_range(node_id=node_id,time_col=time_col)
    if (tmp[1] - tmp[0]) >= timedelta(days=7):
        setting_str = setting_str + '<br>Plotting: most recent 7 days, hourly average'
    else:
        setting_str = setting_str + '<br>Plotting: <b>raw</b>'
    body_text = '<a href=./memory_usage.png>Memory Usage</a>'

    with open(page_template,'r') as f:
        template = Template(f.read())
    tmp = template.render({'title_str':title_str,
                           'node_id':node_id_str,
                           'status_str':status_str,
                           'setting_str':setting_str,
                           'body_text':body_text},
                          TABLE=table,PLOTS=plots)
    with open(output,'w') as f:
        f.write(tmp)


if '__main__' == __name__:
    # don't forget the .css and .js etc.
    output_dir = './www'

    page_template = './template/front_template.html'
    print('Generating front page...')
    gen_front_page(page_template,output_dir)
    
    page_template = './template/node_template.html'
    error_template = './template/error_template.html'
    
    display_config = read_config('display_config.ini',pattern='^node_\d{3}$')
    node_list = display_config.keys()
    html_dirs = [display_config[k]['html_dir'] for k in node_list]
    
    for s,output_path in zip(node_list,html_dirs):
        node_id = int(s[5:8])
        print('Generating webpage for node {}...'.format(node_id))
        gen_node_page(node_id,page_template,error_template,output_path)
    
