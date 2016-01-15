#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

import matplotlib,numpy,traceback
matplotlib.use('Agg')
import sys,re,json,time
sys.path.append('..')
import config
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
from matplotlib.dates import DateFormatter,HourLocator
from config.config_support import *
from os.path import exists,join
from os import makedirs


def PRINT(s):
    print(s)
    #pass


def auto_tick(ax):
    x = ax.get_lines()[0].get_xdata()
    y = ax.get_lines()[0].get_ydata()

    # major tick labels
    # not x[0] and x[-1] because x is not always sorted in ascending order
    # ... ORDER BY ... DESC... because otherwise sqlite will return the first
    # N readings - so if the latest N readings are wanted, they should be at
    # the first N readings (even though they are sorted in descending order)
    # For plotting the oder doesn't matter because every sample has its
    # corresponding timestamp.

    # "locate the earliest timestamp at which time the sample is not an NaN"
    # tricky bastard... nan in numpy.float64 is not float('nan')... and
    # certainly not None, and "is not" won't work either
    begin = min([z[0] for z in zip(x,y) if not numpy.isnan(z[1])])
    end = max(x)
    # why not?
    #end = max([z[0] for z in zip(x,y) if not numpy.isnan(z[1])])

    # show/hide the date in the time axis labels
    if begin.date() == end.date():
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    else:
        ax.xaxis.set_major_formatter(DateFormatter('%b %d %H:%M'))
    plt.gcf().autofmt_xdate()

    # set minor tick density
    ax.yaxis.get_major_formatter().set_useOffset(False)
    timespan = end - begin
    if timespan <= timedelta(days=2):
        ax.xaxis.set_minor_locator(HourLocator(interval=1))
    elif timespan <= timedelta(days=7):
        ax.xaxis.set_minor_locator(HourLocator(interval=3))
    elif timespan <= timedelta(days=14):
        ax.xaxis.set_minor_locator(HourLocator(interval=6))
    elif timespan <= timedelta(days=21):
        ax.xaxis.set_minor_locator(HourLocator(interval=12))
    plt.tight_layout()


def auto_xlabel(ax):
    x = ax.get_lines()[0].get_xdata()
    y = ax.get_lines()[0].get_ydata()

    begin = min([z[0] for z in zip(x,y) if not numpy.isnan(z[1])])
    end = max(x)

    # auto xlabel (time)
    if begin.date() == end.date():
        ax.set_xlabel('UTC Time ({})'.format(begin.strftime('%Y-%m-%d')))
    else:
        ax.set_xlabel('UTC Time ({} to {})'.format(\
            begin.strftime('%Y-%m-%d'),end.strftime('%Y-%m-%d')))


def plot_multi_time_series(data,plotfilename,title='',xlabel='',ylabel=''):
    plt.figure()

    for d in data:
        x = d['x']
        y = d['y']
        try:
            linelabel = d['linelabel']
        except:
            linelabel = None
        try:
            color = d['color']
        except:
            color = None
        try:
            linestyle = d['linestyle']
        except:
            linestyle = ''
        try:
            marker = d['marker']
        except:
            marker = '.'
        try:
            markersize = d['markersize']
        except:
            markersize = 1

        plt.plot_date(x,y,linestyle=linestyle,label=linelabel,color=color,
                      marker=marker,markersize=markersize)

        #import matplotlib.patches as mpatches
        #red_patch = mpatches.Patch()
        #plt.legend(handles=[red_patch])

        #import matplotlib.lines as mlines
        #blue_line = mlines.Line2D([], [], marker='.',
                          #markersize=15, label='stuff')
        #plt.legend(handles=[blue_line])

        plt.legend(loc='best',framealpha=0.5)
        plt.title(title)
        plt.grid(True)

        auto_tick(plt.gca())
        
        if '' == xlabel:
            auto_xlabel(plt.gca())
        else:
            plt.gca().set_xlabel(xlabel)
            
        plt.gca().set_ylabel(ylabel)

    # make the markers in the legend bigger in order to show the color
    try:
        tmp = plt.gca().get_legend()
        for h in tmp.legendHandles:
            h.set_marker('.')
            #h.set_color('red')
            h.set_markersize(8)
    except:
        traceback.print_exc()
    
    plt.savefig(plotfilename,bbox_inches='tight',dpi=300)
    plt.cla()
    plt.clf()
    plt.close()


def plot_time_series(x,y,plotfilename,title='',xlabel='',ylabel='',linelabel=None):
    data = [{'x':x,'y':y,'linelabel':linelabel}]
    plot_multi_time_series(data,plotfilename,
                           title=title,
                           xlabel=xlabel,
                           ylabel=ylabel)


if '__main__' == __name__:
    import sys,traceback,sqlite3,re,importlib,argparse
    sys.path.append('..')
    from storage.storage import storage_read_only
    from scipy.signal import medfilt

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,description='')
    parser.add_argument('--dbfile',type=str,default='./sensor_data.db',metavar='dbfile',help='Path to the database file')
    parser.add_argument('--plot_dir',type=str,default='./gen_plot_output',metavar='plot_dir',help='Output directory for the plots')
    
    args = parser.parse_args()

    # which database to take data from
    dbfile = args.dbfile
    if not exists(dbfile):
        print('dbfile {} not found. Terminating.'.format(dbfile))
        sys.exit()
    else:
        print('Plotting data from {}'.format(dbfile))

    # where to put the generated plots
    plot_dir = args.plot_dir
    PRINT('Output directory: ' + plot_dir)

    store = storage_read_only(dbfile=dbfile)

    IDs = []
    if is_node():
        IDs = [get_node_id()]
    else:
        tmp = store.get_list_of_tables()
        #IDs = [int(t[5:8]) for t in tmp if re.match('^node_\d{3}$',t)]
        IDs = [t.replace('_','-') for t in tmp if re.match('^node.+',t)]

    if len(IDs) <= 0:
        print('Nothing to plot. Terminating.')

    for node_id in IDs:
        PRINT('- - - - -')
        PRINT('node ID:' + node_id)
        node = importlib.import_module('config.' + node_id.replace('-','_'))

        tag_unit_map = get_unit_map(node_id)
        tag_desc_map = get_description_map(node_id)
        node_plot_dir = join(plot_dir,node_id)

        # time_col
        time_col = None
        tmp = store.get_list_of_columns(node_id)
        if 'ReceptionTime' in tmp:
            time_col = 'ReceptionTime'
        elif 'Timestamp' in tmp:
            time_col = 'Timestamp'
        else:
            PRINT('gen_plot.py: no timestamp column found. Skipping this node.')
            continue

        # find the list of variables from config? or from database?
        variables = [c['dbtag'] for c in node.conf if c['plot']]
        plotted = []
        for var in variables:
            timerange = timedelta(hours=node.plot_range)
            cols = [time_col,var]

            title = '{} ({} of {})'.format(tag_desc_map[var],var,node_id)
            plotfilename = join(node_plot_dir,'{}.png'.format(var))

            try:
                tmp = store.read_past_time_period(node_id,time_col,cols,timerange)
                x = tmp[time_col]
                y = [l if l is not None else float('NaN') for l in tmp[var]]

                #y = medfilt(y,5)

                if not exists(node_plot_dir):
                    makedirs(node_plot_dir)

                PRINT('\t{}'.format(var))
                plot_time_series(x,y,plotfilename,title,ylabel=tag_unit_map[var],linelabel=var)

                # save settings of plot to JSON file
                plot_config = {'time_begin':time.mktime(min(x).timetuple()),
                               'time_end':time.mktime(max(x).timetuple()),
                               'plot_generated_at':time.mktime(datetime.utcnow().timetuple()),
                               'data_point_count':len(y)}
                with open(join(node_plot_dir,var + '.json'),'w') as f:
                    # json.dump vs. json.dumps...
                    json.dump(plot_config,f,separators=(',',':'))

                plotted.append(var)

            except (TypeError,sqlite3.OperationalError,ValueError) as e:
                # TypeError: ... I don't remember.
                # sqlite3.OperationalError: db is empty
                # ValueError: db has the variable, but all NaN
                PRINT('\tNo data for {} of {} in the selected range'.\
                      format(var,node_id))
                #traceback.print_exc()
            except:
                traceback.print_exc()

        # website helper
        if exists(node_plot_dir) and len(plotted) > 0:
            with open(join(node_plot_dir,'plotted_var_list.json'),'w') as f:
                tmp = [v + '.png' for v in plotted]
                json.dump(tmp,f,separators=(',',':'))

