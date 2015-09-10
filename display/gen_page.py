#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,pytz,json
sys.path.append('storage')
from jinja2 import Template
from os.path import getmtime,dirname,join,isfile,isdir,exists
from os import remove,rename
from storage import storage
from datetime import datetime,timedelta
from config_support import read_config,read_disp_config,read_capability,is_base,is_node,get_name,get_unit


def PRINT(s):
    #pass
    print(s)

def get_timeago_element(ts = None):
    if ts is None:
        ts = datetime.utcnow()
    ts = ts.replace(tzinfo=pytz.timezone('UTC'))
    #ts = ts.replace(tzinfo=pytz.timezone('America/Los_Angeles'))
    tmp = '<time class="timeago" datetime="{}">ago</time>'.format(ts.isoformat())
    return tmp


def gen_front_page(template_path,output_dir):
    assert isfile(template_path),'gen_front_page(): template_path should point to a file'
    assert isdir(output_dir),'gen_front_page(): output_dir should be a directory'

    # all that to get a node_id:node_name mapping...
    display_config = read_config(pattern='^node_\d{3}$',configini='display_config.ini')
    node_config = read_config('node_config.ini')

    display_config = read_disp_config()
    node_ids = display_config.keys()

    capability = read_capability()
    node_names = [capability[n]['name'] for n in node_ids]
    
    links = ['node_{:03d}.html'.format(n) for n in node_ids]
    disp_str = ['Node #{}, {}'.format(k[0],k[1]) for k in zip(node_ids,node_names)]

    with open(template_path,'r') as f:
        template = Template(f.read())
    html = template.render(NODE_PAGES=zip(links,disp_str))
    with open(join(output_dir,'index.html'),'w') as f:
        f.write(html)


def gen_node_page(node_id,page_template,error_template,output_dir):
    capability = read_capability()
    node_name = get_name(node_id=node_id)

    output = join(output_dir,'node_{:03d}.html'.format(node_id))
    PRINT('Output to: ' + output)

    tmp = read_disp_config()[node_id]
    variables = tmp['variable']
    time_col = tmp['time_col']
    
    if len(variables) <= 0:
        PRINT('gen_node_page(): no variable to tabulate and plot. ABORT')
        with open(error_template,'r') as f:
            template = Template(f.read())
        tmp = template.render({'error_message':'No variable specified in display_config.ini for node_{:03d}'.format(node_id)})
        with open(output,'w') as f:
            f.write(tmp)
        return

    # table of latest readings
    # Retrieve the latest readings, plus Timestamp/ReceptionTime
    # NOTE: On the base station, all database records have associated ReceptionTime but
    # don't always have Timestamp (reported by sensor nodes);
    # BBB nodes have Timestamp but not ReceptionTime;
    # Node #1 and #2 have neither (the optode-only "nodes").
    store = storage()
    try:
        tmp = store.read_latest(node_id,time_col=time_col)
    except Exception as e:
        PRINT('gen_node_page(): error retrieving latest readings, ABORT')
        PRINT(str(sys.exc_info()))
        with open(error_template,'r') as f:
            template = Template(f.read())
        tmp = template.render({'error_message':'Error retrieving latest readings from database.'})
        with open(output,'w') as f:
            f.write(tmp)
        return

    if tmp is None or len(tmp.keys()) <= 0 or len(tmp[tmp.keys()[0]]) <= 0:
        err_msg = 'Database contains no record for node_{:03d}.'.format(node_id)
        PRINT('gen_node_page(): {} ABORT'.format(err_msg))
        with open(error_template,'r') as f:
            template = Template(f.read())
        tmp = template.render({'error_message':err_msg})
        with open(output,'w') as f:
            f.write(tmp)
        return
        
    ts = tmp[time_col][0]
    values = ['{:.2f}'.format(tmp[v][0]) if tmp[v][0] is not None else '-' for v in variables]
    units = get_unit(node_id,variables)
    table = zip(variables,values,units)




    # = = = = = = = = = = = = = = = = = = = =
    # special case for EZO_DO and Pressure_BMP180
    # hack... this is a crime...
    # but not being able to compare mg/L to uM is really annoying
    for k,t in enumerate(table):
        if 'EZO_DO' == t[0]:
            #print t
            # hack like this is gonna get me sooner or later.
            table[k] = (t[0],'{:.2f}'.format(float(t[1])/32e-3),'uM')
        if 'Pressure_BMP180' == t[0]:
            #print t
            table[k] = (t[0],'{:.2f}'.format(float(t[1])/1000.),'kPa')
    # = = = = = = = = = = = = = = = = = = = =




    img_src = ['./node_{:03d}/{}.png'.format(node_id,var) for var in variables]

    # another kitten killed.
    tmp = ['./www/node_{:03d}/{}.json'.format(node_id,v) for v in variables]
    plot_config = [json.load(open(p,'r')) if exists(p) else None for p in tmp]

    img_header = []
    for c in plot_config:
        plot_type = c['plot_type']
        time_begin = datetime.fromtimestamp(c['time_begin'])
        time_end = datetime.fromtimestamp(c['time_end'])
        plot_generated_at = datetime.fromtimestamp(c['plot_generated_at'])
        tmp = (time_end - time_begin).total_seconds()
        nday,remain = divmod(tmp,24*60*60)

        header_str = ''
        if nday > 0:
            header_str = header_str + '{:.0f}d {:.1f}hr'.format(nday,remain/3600.)
        else:
            header_str = header_str + '{:.0f}hr'.format(remain/3600.)

        if 'raw' == plot_type:
            header_str = header_str + ', raw'
        elif 'hourly' == plot_type:
            header_str = header_str + ', hourly average'
        elif 'daily' == plot_type:
            header_str = header_str + ', daily average'
        else:
            PRINT('gen_page: gen_node_page(): huh?')

        header_str = header_str + ' (generated {})'.format(get_timeago_element(plot_generated_at))

        img_header.append(header_str)

    #img_header = variables
    img_alt = variables
    img_link_to = ['experimental/gen_var_page.py?node_id={}&nhour=1&var={}'.format(node_id,v) for v in variables]
    plots = zip(img_header,img_src,img_alt,img_link_to)

    node_id_str = 'Node #{}, {}'.format(node_id,node_name)
    title_str = node_id_str
    timeelement = get_timeago_element(ts)
    status_str = 'Last reading sampled at {} UTC ({})'.format(ts.strftime('%Y-%m-%d %H:%M:%S'),timeelement)
    #setting_str = 'Median filter: {}'.format('<b>OFF</b>')
    setting_str = ''
    
    with open(page_template,'r') as f:
        template = Template(f.read())
    tmp = template.render({'title_str':title_str,
                           'node_id_str':node_id_str,
                           'status_str':status_str,
                           'setting_str':setting_str},
                          TABLE=table,PLOTS=plots)
    with open(output,'w') as f:
        f.write(tmp)
    return output


if '__main__' == __name__:
    # don't forget the .css and .js etc.
    output_dir = './www'

    page_template = './template/node_template.html'
    error_template = './template/error_template.html'
    tmp = read_disp_config()
    node_ids = tmp.keys()
    html_dirs = [tmp[k]['html_dir'] for k in node_ids]
    node_page_file = '' # if is_node(), this loop runs only once
    for node_id,output_path in zip(node_ids,html_dirs):
        PRINT('Generating webpage for node {}...'.format(node_id))
        node_page_file = gen_node_page(node_id,page_template,error_template,output_path)
    if is_base():
        page_template = './template/front_template.html'
        PRINT('Generating front page...')
        gen_front_page(page_template,output_dir)
    elif is_node():
        tmp = join(output_dir,'index.html')
        try:
            remove(tmp)
        except:
            pass
        rename(node_page_file,tmp)
    else:
        print('sobbing mathematically')
        
