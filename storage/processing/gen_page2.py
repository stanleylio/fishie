# -*- coding: utf-8 -*-
import calendar,traceback
from jinja2 import Template
from json import dumps
from storage import storage_read_only
from helper import *
from datetime import datetime
from os import makedirs
from os.path import join
from shutil import copy2


def g(template,output,table,time_col,variable):
    store = storage_read_only(dbfile='sensor_data.db')
    tmp = store.read_all(table,cols=[time_col,variable])
    if tmp is None:
        print('table {} is empty'.format(table))
        return
    print('{} samples'.format(len(tmp[variable])))
    ts = [dt2ts(v) for v in tmp[time_col]]
    #ts = tmp[time_col]
    x = tmp[variable]
    if isinstance(x[0],datetime):
        print(variable + ' is datetime, ignore')
        return
    x = [xx if xx is not None else float('nan') for xx in x]

    #from helper import median_of_group
    #ts,x = median_of_group(ts,x)
    xlabel = 'Date/Time'
    ylabel = 'ylabel'
    title = table
    linelabel = ''
    # - - - - -

    ts = dumps(ts,separators=(',',':'))
    x = dumps(x,separators=(',',':'))
    xlabel = dumps(xlabel)
    ylabel = dumps(ylabel)
    title = dumps(title)
    linelabel = dumps(linelabel)

    with open(template,'r') as f,\
         open(output,'w') as fout:
        t = Template(f.read())
        s = t.render(ts=ts,x=x,xlabel=xlabel,ylabel=ylabel,title=title,linelabel=linelabel)
        fout.write(s)


if '__main__' == __name__:
    template = 'template.html'

    store = storage_read_only()
    store.print_schema()
    print
    
    for table in store.get_list_of_tables():
        try:
            d = join('output',table)
            makedirs(d)
        except:
            traceback.print_exc()
        try:
            copy2('jquery.min.js',join('output','jquery.min.js'))
            copy2('plotly-latest.min.js',join('output','plotly-latest.min.js'))
        except:
            traceback.print_exc()
        
        tmp = store.get_list_of_columns(table)

        time_col = None
        if 'Timestamp' in tmp:
            time_col = 'Timestamp'
        if 'ReceptionTime' in tmp:
            time_col = 'ReceptionTime'

        if time_col is not None:
            for variable in tmp:
                print table,variable,time_col
                output = join('output',table,'{}-{}.html').format(table,variable)
                g(template,output,table,time_col,variable)



