#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

import matplotlib
matplotlib.use('Agg')
import sys,re,json,time
sys.path.append('../storage')
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
from matplotlib.dates import DateFormatter,HourLocator
#from numpy import ndarray
#import numpy as np

from storage import storage_read_only
from config_support import *
from os.path import exists,join
from os import makedirs


def PRINT(s):
    print(s)
    #pass


def plot_time_series(x,y,plotfilename,title='',xlabel='',ylabel='',linelabel=None):
    plt.figure()
    plt.plot_date(x,y,linestyle='-',label=linelabel,color='b',marker='.',markersize=4)
    plt.legend(loc='best',framealpha=0.5)
    plt.title(title)
    plt.grid(True)

    # major tick labels
    # not x[0] and x[-1] because x is not always sorted in ascending order
    # ... ORDER BY ... DESC... because otherwise sqlite will return the first
    # N readings - so if the latest N readings are wanted, they should be at
    # the first N readings (even though they are sorted in descending order)
    # For plotting the oder doesn't matter because every sample has its
    # corresponding timestamp.
    begin = min(x)
    end = max(x)

    timespan = end - begin
    if begin.date() == end.date():
        plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))
    else:
        plt.gca().xaxis.set_major_formatter(DateFormatter('%b %d %H:%M'))
    plt.gcf().autofmt_xdate()

    # minor tick density
    plt.gca().yaxis.get_major_formatter().set_useOffset(False)
    if timespan <= timedelta(days=2):
        plt.gca().xaxis.set_minor_locator(HourLocator(interval=1))
    elif timespan <= timedelta(days=7):
        plt.gca().xaxis.set_minor_locator(HourLocator(interval=3))
    elif timespan <= timedelta(days=14):
        plt.gca().xaxis.set_minor_locator(HourLocator(interval=6))
    elif timespan <= timedelta(days=21):
        plt.gca().xaxis.set_minor_locator(HourLocator(interval=12))
    plt.tight_layout()

    # auto xlabel (time)
    if '' == xlabel:
        if begin.date() == end.date():
            plt.gca().set_xlabel('UTC Time ({})'.format(begin.strftime('%Y-%m-%d')))
        else:
            plt.gca().set_xlabel('UTC Time ({} to {})'.format(\
                begin.strftime('%Y-%m-%d'),end.strftime('%Y-%m-%d')))
    else:
        plt.gca().set_xlabel(xlabel)
        
    plt.gca().set_ylabel(ylabel)
        
    plt.savefig(plotfilename,bbox_inches='tight',dpi=300)
    plt.cla()
    plt.clf()
    plt.close()


if '__main__' == __name__:
    import traceback,sqlite3
    from scipy.signal import medfilt

    IDs = []
    time_col = None
    if is_base():
        IDs = get_list_of_nodes()
        time_col = 'ReceptionTime'
    elif is_node():
        IDs = [get_node_id()]
        time_col = 'Timestamp'

    assert time_col is not None

    for node_id in IDs:
        PRINT('- - - - -')
        node_tag = 'node-{:03d}'.format(node_id)
        config_file = '../config/{}.ini'.format(node_tag)

        tags = get_tag(node_id)
        units = get_unit(node_id)
        mapping = dict(zip(tags,units))

        store = storage_read_only()
        
        config = read_ini(config_file)['display']
        plot_dir = config['plot_dir']
        plot_dir = join(plot_dir,node_tag)
        if not exists(plot_dir):
            makedirs(plot_dir)

        try:
            plot_range = int(config['plot_range'])
        except:
            PRINT('gen_plot.py: plot_range not specified. Use default')
            plot_range = 3*24
        
        variables = [c.strip() for c in config['variable'].split(',')]
        for var in variables:
            unit = mapping[var]

            timerange = timedelta(hours=plot_range)
            cols = [time_col,var]
            
            title = '{} of {}'.format(var,node_tag)
            plotfilename = join(plot_dir,'{}.png'.format(var))

            try:
                #tmp = store.read_latest(node_id,time_col,variables,count)
                tmp = store.read_time_range(node_id,time_col,cols,timerange)
                x = tmp[time_col]
                y = [l if l is not None else float('NaN') for l in tmp[var]]

                y = medfilt(y,9)

                PRINT('Plotting {} of {}...'.format(var,node_tag))
                plot_time_series(x,y,plotfilename,title,ylabel=unit,linelabel=var)

                # save settings of plot to JSON file
                plot_config = {'time_begin':time.mktime(min(x).timetuple()),
                               'time_end':time.mktime(max(x).timetuple()),
                               'plot_generated_at':time.mktime(datetime.utcnow().timetuple()),
                               'data_point_count':len(y)}
                with open(join(plot_dir,var + '.json'),'w') as f:
                    # json.dump vs. json.dumps...
                    json.dump(plot_config,f,separators=(',',':'))

            except (TypeError,sqlite3.OperationalError,ValueError) as e:
                # TypeError: ... I don't remember.
                # sqlite3.OperationalError: db is empty
                # ValueError: db has the variable, but all NaN
                #print traceback.print_exc()
                PRINT('No data for {} of {} in the selected range'.\
                      format(var,node_tag))

