#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015
import matplotlib,numpy,traceback
matplotlib.use('Agg')
import sys
#sys.path.append('..')
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
from matplotlib.dates import DateFormatter,HourLocator
#from config.config_support import *


def auto_tick(ax):
    x = ax.get_lines()[0].get_xdata()
    y = ax.get_lines()[0].get_ydata()

    # major tick labels
    # Not x[0] and x[-1] because x is not always sorted in ascending order.
    #
    # ... ORDER BY ... DESC... because otherwise sqlite will return the first
    # N readings - so if the latest N readings are wanted, they should be at
    # the first N readings (even though they are sorted in descending order)
    # For plotting the order doesn't matter because the samples are timestamped.

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
            color = 'blue'
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

        #print(color,linestyle,marker,markersize)

        plt.plot_date(x,y,
                      linestyle=linestyle,
                      label=linelabel,
                      color=color,
                      marker=marker,
                      markersize=markersize)

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
        #auto_xlabel(plt.gca())
        begin = data[0]['x'][0]
        end = begin
        for d in data:
            x,y = d['x'],d['y']
            b = min([z[0] for z in zip(x,y) if not numpy.isnan(z[1])])
            if b < begin:
                begin = b
            e = max([z[0] for z in zip(x,y) if not numpy.isnan(z[1])])
            if e > end:
                end = e
        plt.gca().set_xlabel('UTC Time ({} to {})'.\
                             format(begin.strftime('%Y-%m-%d'),\
                                    end.strftime('%Y-%m-%d')))
    else:
        plt.gca().set_xlabel(xlabel)
        
    plt.gca().set_ylabel(ylabel)

    # make the markers in the legend bigger in order to show the color
    try:
        tmp = plt.gca().get_legend()
        if tmp is not None:
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


def plot_time_series(x,y,plotfilename,title='',xlabel='',ylabel='',linelabel=None,markersize=1):
    assert len(x) == len(y)
    assert len(plotfilename) > 0
    
    data = [{'x':x,'y':y,'linelabel':linelabel,'markersize':markersize}]

    if '' == xlabel:
        begin = min([z[0] for z in zip(x,y) if not numpy.isnan(z[1])])
        end = max([z[0] for z in zip(x,y) if not numpy.isnan(z[1])])
        if begin.date() == end.date():
            xlabel = 'UTC Time ({})'.format(begin.strftime('%Y-%m-%d'))
        else:
            xlabel = 'UTC Time ({} to {})'.\
                     format(begin.strftime('%Y-%m-%d'),\
                            end.strftime('%Y-%m-%d'))

    plot_multi_time_series(data,plotfilename,
                           title=title,
                           xlabel=xlabel,
                           ylabel=ylabel)

