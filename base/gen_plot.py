#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

import matplotlib
matplotlib.use('Agg')
import sys,argparse,re
sys.path.append('storage')
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
from matplotlib.dates import DateFormatter,HourLocator
from os.path import exists,join,dirname
from os import makedirs
from storage import storage
from scipy.signal import medfilt
from numpy import ndarray
import numpy as np
from parse_support import read_capability
from ConfigParser import RawConfigParser,NoSectionError

def PRINT(s):
    #pass
    print(s)

# time series plot, assume x is a list of timestamps
# this generates one plot, with possible mutiple y lines in the same plot
def plot_time_series(d,title,xlabel,ylabel,plotfilename):
    x = d['x']
    y = d['y']
    try:
        linestyle = d['linestyle']
    except KeyError:
        linestyle = 'r'
    try:
        linelabel = d['linelabel']
    except KeyError:
        linelabel = ''

    # y etc. can be list of readings, or could be list of list of readings.
    # in the latter case, one line per list all on the same plot
    plt.figure()
    if type(y[0]) is list or type(y[0]) is ndarray:
        tmp = zip(y,linestyle,linelabel)
    else:
        tmp = [(y,linestyle,linelabel)]
    for p in tmp:
        plt.plot_date(x,p[0],p[1],label=p[2])
        plt.legend(loc='best',framealpha=0.5)

    # min, max, (mean?)
    xmin = min(x)
    xmax = max(x)
    ymin = min([min(v[0]) for v in tmp])
    ymax = max([max(v[0]) for v in tmp])
    xp = x[int(round(0.3*len(x)))]
    plt.plot([xmin,xmax],[ymin,ymin],'k--')
    plt.gca().annotate('{:.2f}'.format(ymax),xy=(xp,ymax),xytext=(xp,ymax),\
                       va='bottom',ha='center')
    plt.plot([xmin,xmax],[ymax,ymax],'k--')
    plt.gca().annotate('{:.2f}'.format(ymin),xy=(xp,ymin),xytext=(xp,ymin),\
                       va='top',ha='center')
    
    plt.title(title)
    plt.grid(True)

    # major tick labels
    begin = x[0]
    end = x[-1]
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

    # dynamic xlabel (time)
    if xlabel is None:
        plt.gca().set_ylabel(ylabel)
        if begin.date() == end.date():
            plt.gca().set_xlabel('Time ({})'.format(begin.strftime('%Y-%m-%d')))
        else:
            plt.gca().set_xlabel('Time ({} to {})'.format(\
                begin.strftime('%Y-%m-%d'),end.strftime('%Y-%m-%d')))

    plt.savefig(plotfilename,bbox_inches='tight',dpi=300)
    plt.cla()
    plt.clf()
    plt.close()


if '__main__' == __name__:
    desc_str = '''Plot a sequence of time series data in a PNG file. Example:
\tpython gen_plot.py -i 4 -v Temp_BMP180 -p /var/www
Name of variable is the same as the name of the column in the database.'''
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,\
                                     description=desc_str)
#    parser.add_argument('-f',type=str,metavar='DATA_FILE',help='path to a time series CSV')
    parser.add_argument('-i','--id',type=int,metavar='ID',help='Node ID, an integer')
    parser.add_argument('-v','--var',type=str,metavar='VAR',\
                        help='name of the variable to plot')
    parser.add_argument('-p',type=str,metavar='PLOT_DIR',help='directory for the plots')
    args = parser.parse_args()

    plot_list = {}
    var = args.var
    node_id = args.id
    plot_dir = args.p
    if node_id is not None:
        if plot_dir is None:
            plot_dir = '.'
        plot_list[node_id] = {}
        plot_list[node_id]['plot_dir'] = plot_dir
        plot_list[node_id]['var_list'] = [var]
        plot_list[node_id]['linestyle'] = ['b']
    else:
        parser = RawConfigParser()
        parser.read(join(dirname(__file__),'display_config.ini'))
        for s in parser.sections():
            if re.match('^node_\d{3}$',s):
                node_id = int(s[5:8])
                plot_list[node_id] = {}
                plot_list[node_id]['plot_dir'] = parser.get(s,'plot_dir')
                plot_list[node_id]['time_col'] = parser.get(s,'time_col')
                plot_list[node_id]['var_list'] = parser.get(s,'variable').split(',')
                plot_list[node_id]['linestyle'] = parser.get(s,'linestyle').split(',')

    # - - - - -
    
    store = storage()

    for node in plot_list.keys():
        plot_dir = plot_list[node_id]['plot_dir']
        var_list = plot_list[node_id]['var_list']
        time_col = plot_list[node_id]['time_col']
        linestyles = plot_list[node_id]['linestyle']

        if not exists(plot_dir):
            makedirs(plot_dir)

        for var,linestyle in zip(var_list,linestyles):
            #print node_id,var
            node_capability = read_capability()
            dbtag = node_capability[node_id]['dbtag']
            dbunit = node_capability[node_id]['dbunit']
            unit = dict(zip(dbtag,dbunit))[var]
            col_name = [time_col,var]

            #tmp = store.read_all(node_id,col_name,time_col=time_col)
            #tmp = store.read_latest(node_id,col_name,count=8000,time_col=time_col)
            #tmp = store.read_latest(node_id,col_name,nhour=3*24,time_col=time_col)

            # hourly_average() gives you a sequence of timestamps, so skip the first tag.
            tmp = store.hourly_average(node_id,col_name=col_name[1:],time_col=time_col)
            TS = tmp[time_col]
            readings = tmp[var]

            PRINT('Plotting {} of node_{:03d}...'.format(var,node_id))
            tmp = {'x':TS,'y':readings,'linestyle':linestyle,'linelabel':var}
            plot_time_series(tmp,'{} of node_{:03d}'.\
                     format(var,node_id),None,unit,\
                     join(plot_dir,var + '.png'))

            
