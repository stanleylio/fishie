#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015
import matplotlib
matplotlib.use('Agg')
import numpy as np
import sys, logging, pytz
from os.path import expanduser
sys.path.append(expanduser('~'))
from node.helper import ts2dt
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter, HourLocator, num2date


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
    # nan in np.float64 is not float('nan')... and
    # certainly not None, and "is not" won't work either
    nonnull = [z[0] for z in zip(x,y) if not np.isnan(z[1])]
    if len(nonnull) <= 0:
        logging.debug('no data or all NaNs')
        return
    begin = min(nonnull)
    end = max(x)
    # why not?
    #end = max([z[0] for z in zip(x,y) if not np.isnan(z[1])])

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


def plot_multi_time_series(data, plotfilename, *, title='', xlabel='', ylabel='', loc='best'):
    plt.figure()

    for d in data:
        # maybe use python's own kargs instead? TODO
        x = d['x']
        y = d['y']
        sun = d['sun']
        label = d.get('linelabel', None)
        color = d.get('color', None)
        linestyle = d.get('linestyle', '')
        marker = d.get('marker', '.')
        markersize = d.get('markersize', 1)

        #print x[0]
        #print type(x[0])

        if type(x[0]) is not datetime:
            x = [ts2dt(tmp) for tmp in x]
        
        #print(color,linestyle,marker,markersize)

        ax = plt.subplot()
        ax.plot_date(x,
                     y,
                     linestyle=linestyle,
                     label=label,
                     color=color,
                     marker=marker,
                     markersize=markersize)

        if sun is not None and len(sun):
            #print(sun)
            #for tmp in sun:
            #    print(tmp)
            xmin, xmax = ax.get_xlim()
            xmin = num2date(xmin)
            xmax = num2date(xmax)
            #print(xmin, xmax)
            # Easier to just trim the ends. In dense plot the X limits sometimes
            # extend past the previous sunrise / next sunset, so only take the
            # newly added sunrise/sunset limits up to the X limits.
            sun = sorted(sun, key=lambda tmp: tmp[0])
            if not sun[0][1]:   # first item is a sunset
                #sun.pop(0)
                tmp = min(x).replace(tzinfo=pytz.utc)
                tmp = max(tmp, xmin)
                sun.insert(0, (tmp, True))
            if sun[-1][1]:      # last item is a sunrise
                #sun.pop(len(sun) - 1)
                tmp = max(x).replace(tzinfo=pytz.utc)
                tmp = min(tmp, xmax)
                sun.append((tmp, False))
            #print()
            #for tmp in sun:
            #    print(tmp)

            # assert: not len(sun) % 2

            for a, b in zip(sun[0::2], sun[1::2]):
                ax.axvspan(a[0], b[0], facecolor='lightskyblue', alpha=0.2)

        #import matplotlib.patches as mpatches
        #red_patch = mpatches.Patch()
        #plt.legend(handles=[red_patch])

        #import matplotlib.lines as mlines
        #blue_line = mlines.Line2D([], [], marker='.',
                          #markersize=15, label='stuff')
        #plt.legend(handles=[blue_line])

    plt.legend(loc=loc, framealpha=0.5)
    plt.title(title)
    plt.grid(True)

    auto_tick(plt.gca())
    
    if '' == xlabel:
        #auto_xlabel(plt.gca())
        #begin = data[0]['x'][0]
        begin = x[0]
        end = begin
        for d in data:
            #x,y = d['x'],d['y']
            b = min([z[0] for z in zip(x,y) if not np.isnan(z[1])])
            if b < begin:
                begin = b
            e = max([z[0] for z in zip(x,y) if not np.isnan(z[1])])
            if e > end:
                end = e
        plt.gca().set_xlabel('UTC Time ({} to {})'.\
                             format(begin.strftime('%Y-%m-%d'),\
                                    end.strftime('%Y-%m-%d')))
    else:
        plt.gca().set_xlabel(xlabel)
        
    plt.gca().set_ylabel(ylabel)

    # make the markers in the legend bigger in order to show the color
    tmp = plt.gca().get_legend()
    if tmp is not None:
        for h in tmp.legendHandles:
            h.set_marker('.')
            #h.set_color('red')
            h.set_markersize(8)

    plt.savefig(plotfilename, bbox_inches='tight', dpi=600, facecolor='#f2f2f2')
    #print(plotfilename)
    plt.cla()
    plt.clf()
    plt.close()


def plot_time_series(x, y, plotfilename, *_, sun=None, title='', xlabel='', ylabel='', linelabel=None, color='#1f77b4', linestyle='-', marker='.', markersize=1):
    assert len(x) == len(y)
    assert len(x) > 0
    assert len(plotfilename) > 0

    # replace any None with float('nan')
    y = [yy if yy is not None else float('nan') for yy in y]

    # locate the start and end dates on which the data is not float('nan')
    if '' == xlabel:
        z = zip(x, y)
        z = [zz[0] for zz in z]
        begin = min(z)
        end = max(z)
        if type(begin) is float:
            begin = ts2dt(begin)
        if type(end) is float:
            end = ts2dt(end)
        if begin.date() == end.date():
            xlabel = 'UTC Time ({})'.format(begin.strftime('%Y-%m-%d'))
        else:
            xlabel = 'UTC Time ({} to {})'.\
                     format(begin.strftime('%Y-%m-%d'),\
                            end.strftime('%Y-%m-%d'))

    data = [{'x':x,
             'y':y,
             'sun':sun,
             'linelabel':linelabel,
             'color':color,
             'linestyle':linestyle,
             'marker':marker,
             'markersize':markersize}]
    
    plot_multi_time_series(data,
                           plotfilename,
                           title=title,
                           xlabel=xlabel,
                           ylabel=ylabel)

