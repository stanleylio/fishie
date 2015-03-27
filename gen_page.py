#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,pytz,json
sys.path.append('storage')
from jinja2 import Template
from os.path import getmtime,dirname,join,isfile,isdir,exists
from storage import storage
from datetime import datetime,timedelta
from parse_support import read_capability,read_disp_config,read_config


def PRINT(s):
    #pass
    print(s)


def gen_front_page(template_path,output_dir):
    assert isfile(template_path),'gen_front_page(): template_path should point to a file'
    assert isdir(output_dir),'gen_front_page(): output_dir should be a directory'

    # all that to get a node_id:node_name mapping...
    display_config = read_config('display_config.ini',pattern='^node_\d{3}$')
    node_config = read_config('node_config.ini')

    display_config = read_disp_config()
    node_ids = display_config.keys()

    capability = read_capability()
    node_names = [capability[n]['name'] for n in node_ids]
    
    links = ['node_{:03d}.html'.format(n) for n in node_ids]
    disp_str = ['Node #{}, {}'.format(k[0],k[1]) for k in zip(node_ids,node_names)]

    with open(template_path,'r') as f:
        template = Template(f.read())
    tmp = template.render(NODE_PAGES=zip(links,disp_str))
    with open(join(output_dir,'index.html'),'w') as f:
        f.write(tmp)


def gen_node_page(node_id,page_template,error_template,output_dir):
    capability = read_capability()
    node_name = capability[node_id]['name']
    dbtag = capability[node_id]['dbtag']
    dbunit = capability[node_id]['dbunit']
    units = dict(zip(dbtag,dbunit))

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

    # Retrieve the latest readings, plus Timestamp/ReceptionTime
    # NOTE: On the base station, all database records have associated ReceptionTime but
    # don't always have Timestamp (reported by sensor nodes); on nodes they may have neither.
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
    values = ['{:.2f}'.format(tmp[v][0]) if tmp[v][0] is not None else '-' for v in variables]
    units = [units[v] for v in variables]
    table = zip(variables,values,units)




    # = = = = = = = = = = = = = = = = = = = =
    # special case for EZO_DO and Pressure_BMP180
    # I have just commited a CRIME
    # but not being able to compare mg/L to uM is really annoying
    for k,t in enumerate(table):
        if 'EZO_DO' == t[0]:
            print t
            # hack like this is gonna get me sooner or later.
            table[k] = (t[0],'{:.2f}'.format(float(t[1])/32e-3),'uM')
        if 'Pressure_BMP180' == t[0]:
            print t
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
        tmp = (time_end - time_begin).total_seconds()
        nday,remain = divmod(tmp,24*60*60)

        header_str = ''
        if nday > 0:
            header_str = header_str + '{:.0f}d {:.1f}hr'.format(nday,remain/3600.)
        else:
            header_str = header_str + '{:.0f}hr'.format(remain/3600.)

        if 'raw' == plot_type:
            header_str = header_str + ', Raw'
        elif 'hourly' == plot_type:
            header_str = header_str + ', Hourly Average'
        elif 'daily' == plot_type:
            header_str = header_str + ', Daily Average'
        else:
            print 'gen_page: gen_node_page(): huh?'
            pass

        img_header.append(header_str)
    
    #img_header = variables
    
    img_alt = variables
    plots = zip(img_header,img_src,img_alt)

    ts = ts.replace(tzinfo=pytz.timezone('UTC'))
    #ts = ts.replace(tzinfo=pytz.timezone('America/Los_Angeles'))

    node_id_str = 'Node #{} ({})'.format(node_id,node_name)
    title_str = node_id_str
    timeelement = '<time class="timeago" datetime="{}">ago</time>'.format(ts.isoformat())
    status_str = 'Last reading sampled at {} UTC ({})'.format(ts.strftime('%Y-%m-%d %H:%M:%S'),timeelement)
    #status_str = 'Last reading in plot sampled at {} PST ({})'.format(ts.strftime('%Y-%m-%d %H:%M:%S'),timeelement)
    setting_str = 'Median filter: {}'.format('<b>OFF</b>')
# TODO: every time you use a magic number god kills a kitten.
    tmp = store.read_time_range(node_id=node_id,time_col=time_col)
    if (tmp[1] - tmp[0]) >= timedelta(days=7):
        setting_str = setting_str + '<br>Plotting: most recent 7 days, hourly average'
    else:
        setting_str = setting_str + '<br>Plotting: <b>raw</b>'

    with open(page_template,'r') as f:
        template = Template(f.read())
    tmp = template.render({'title_str':title_str,
                           'node_id':node_id_str,
                           'status_str':status_str,
                           'setting_str':setting_str},
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
    
