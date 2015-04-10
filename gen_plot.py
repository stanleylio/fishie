#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

import matplotlib
matplotlib.use('Agg')
import sys,re,json,time
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
from config_support import get_unit,read_config,read_disp_config


def PRINT(s):
    #pass
    print(s)

# time series plot, assume x is a list of timestamps
# this generates one plot, with possible mutiple y lines in the same plot
def plot_time_series(d,title,xlabel,ylabel,plotfilename):
    x = d['x']
    y = d['y']
    try:
        linelabel = d['linelabel']
    except KeyError:
        linelabel = ''      # don't think this work for the multi-line case. TODO
    try:
        linestyle = d['linestyle']
    except KeyError:
        linestyle = ['-' for l in linelabel]
    try:
        linecolor = d['linecolor']
    except KeyError:
        linecolor = ['r' for l in linelabel]

    # y etc. can be list of readings, or could be list of list of readings.
    # in the latter case, one line per list all on the same plot
    plt.figure()
    if type(y[0]) is list or type(y[0]) is ndarray:
        tmp = zip(y,linestyle,linelabel,linecolor)
    else:
        tmp = [(y,linestyle,linelabel,linecolor)]
    for p in tmp:
        plt.plot_date(x,p[0],linestyle=p[1],label=p[2],color=p[3],marker=None)
        plt.legend(loc='best',framealpha=0.5)

    # min, max, (mean?)
    xmin = min(x)
    xmax = max(x)
    ymin = min([min(v[0]) for v in tmp])
    ymax = max([max(v[0]) for v in tmp])
    xp = x[int(round(0.3*len(x)))]
    if all([v is not None for v in [xmin,xmax,ymin,ymax]]):
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

    plt.savefig(plotfilename,bbox_inches='tight',dpi=150)
    plt.cla()
    plt.clf()
    plt.close()


if '__main__' == __name__:
    display_config = read_disp_config()

    store = storage()

    for node_id in sorted(display_config.keys()):
        tmp = read_disp_config()    # can use JSON, XML or pickle.
        plot_dir = tmp[node_id]['plot_dir']
        time_col = tmp[node_id]['time_col']
        var_list = tmp[node_id]['variable']
        linestyles = tmp[node_id]['linestyle']
        linecolors = tmp[node_id]['linecolor']

        if not exists(plot_dir):
            makedirs(plot_dir)

        for var,linestyle,linecolor in zip(var_list,linestyles,linecolors):
            unit = get_unit(node_id,var)
            col_name = [time_col,var]

            #tmp = store.read_all(node_id,col_name,time_col=time_col)
            #tmp = store.read_latest(node_id,col_name,count=8000,time_col=time_col)
            #tmp = store.read_latest(node_id,col_name,nhour=3*24,time_col=time_col)
            # hourly_average() gives you a sequence of timestamps, so don't need to specify
            # the timestamp column in col_name
            #tmp = store.hourly_average(node_id,col_name=col_name[1:],time_col=time_col)

            # TODO move this to config file too
            plot_range = 7  # days

            time_range = store.read_time_range(node_id,time_col=time_col)
            plot_type = '-'
            if None not in time_range:
                if (time_range[1] - time_range[0]) >= timedelta(days=plot_range):
                    plot_type = 'hourly'
                    tmp = store.read(node_id,variables=col_name[1:],nday=plot_range,time_col=time_col,avg='hourly')
#                    tmp = store.read(node_id,variables=col_name[1:],nhour=1,time_col=time_col)
                else:
                    plot_type = 'raw'
                    tmp = store.read(node_id,variables=col_name[1:],time_col=time_col)
            else:
                tmp = None

            if tmp is None or len(tmp) <= 0 or len(tmp[time_col]) <= 0:
                PRINT('gen_plot: database contains no record for node_{:03d}. ABORT'.format(node_id))
                break
            
            TS = tmp[time_col]
            readings = tmp[var]




            # = = = = = = = = = = = = = = = = = = = =
            # special case for EZO_DO and Pressure_BMP180
            # "every time you make a hack god kills a kitten"
            # but not being able to compare mg/L to uM is really annoying
            if 'EZO_DO' == var:
                readings = [v/32e-3 for v in readings]
                unit = 'uM'
            elif 'Pressure_BMP180' == var:
                readings = [v/1000. for v in readings]
                unit = 'kPa'
            else:
                pass
            # = = = = = = = = = = = = = = = = = = = =




            # the beef
            PRINT('Plotting {} of node_{:03d}...'.format(var,node_id))
            tmp = {'x':TS,'y':readings,'linestyle':linestyle,'linelabel':var,'linecolor':linecolor}
            plot_time_series(tmp,'{} of node_{:03d}'.\
                     format(var,node_id),None,unit,\
                     join(plot_dir,var + '.png'))

            # save settings of plot to disk
            plot_config = {'plot_type':plot_type,
                           'time_begin':time.mktime(min(TS).timetuple()),
                           'time_end':time.mktime(max(TS).timetuple()),
                           'plot_generated_at':time.mktime(datetime.utcnow().timetuple())}
            with open(join(plot_dir,var + '.json'),'w') as f:
                # json.dump vs. json.dumps...
                json.dump(plot_config,f,separators=(',',':'))
                

