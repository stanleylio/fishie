# loko i'a app "weekly and monthly plots"
#
# Stanley H.I. Lio
# hlio@soest.hawaii.edu
# All Rights Reserved. 2017
import sys, traceback, json, time, math, logging, argparse, numpy
from os import makedirs
from os.path import exists, join, expanduser
sys.path.append(expanduser('~'))
from datetime import datetime, timedelta
from scipy.signal import medfilt
from node.helper import dt2ts
from node.display.gen_plot import plot_time_series
from node.storage.storage2 import Storage, auto_time_col
from node.config.config_support import get_list_of_nodes, get_list_of_disp_vars, get_description, get_unit


logging.basicConfig(level=logging.DEBUG)


def is_node(device):
    return not device.startswith('base-')


def poh_preferred_unit_conversion(node, var, readings):
    if 'node-025' == node and 'salinity_seabird' == var:
        unit = 'ppt'
    elif node in ['node-004'] and 'O2Concentration' == var:
        unit = 'mg/L'
        # http://ocean.ices.dk/Tools/UnitConversion.aspx
        readings = [tmp*0.032 for tmp in readings]
    elif 'node-007' == node and 'Wind_average' == var:
        unit = 'knot'
        readings = [tmp*1.94384 for tmp in readings]
    else:
        unit = get_unit(node,var)
    return readings,unit


def p(node, var, time_col, begin, end, outputdir):
    r = store.read_time_range(node, time_col, [time_col, var], begin, end)
    assert r is not None
    print('\t' + var)

    # strip all "None" and "NaN"
    tmp = zip(r[time_col], r[var])
    tmp = filter(lambda x: x[1] is not None, tmp)
    tmp = list(filter(lambda x: not numpy.isnan(x[1]), tmp))
    if len(tmp) <= 0:
        logging.info('No data to plot')
        return
    # ... and if there's still stuff left to plot,
    x, y = zip(*tmp)
    
    var_description = get_description(node, var)
    title = '{} ({} of {})'.format(var_description, var, node)
    y,unit = poh_preferred_unit_conversion(node, var, y)
    if unit is None:
        ylabel = '(unitless)'
    else:
        ylabel = unit

    # remove spikes if any
    y = medfilt(y,21)
    plot_time_series(x,y,\
                     join(outputdir,var + '.png'),\
                     title=title,\
                     ylabel=ylabel,\
                     linelabel=var)

    plot_config = {'time_begin':min(x),
                   'time_end':max(x),
                   'plot_generated_at':dt2ts(),
                   'data_point_count':len(list(filter(lambda yy: yy is not None and not math.isnan(yy), y))),
                   'unit':unit,
                   'description':var_description}
    with open(join(outputdir,var + '.json'),'w') as f:
        json.dump(plot_config,f,separators=(',',':'))


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,description='')
parser.add_argument('--site',type=str,default='poh',metavar='site',help='Name of the site.')
args = parser.parse_args()

site = args.site
logging.info('Site = {}'.format(site))
plot_dir = '/var/www/uhcm/img'
logging.info('Output dir = ' + plot_dir)

assert exists(plot_dir)
plot_dir = join(plot_dir,site)
if not exists(plot_dir):
    makedirs(plot_dir)


store = storage()
list_of_nodes = get_list_of_nodes(site)
for node in list_of_nodes:
    if not is_node(node):   # could be a base station or other stuff in the future
        continue

    # auto-select a column as time
    V = get_list_of_disp_vars(node)
    try:
        columns = store.get_list_of_columns(node)
    except:
        traceback.print_exc()
        continue
    assert set(V) <= set(columns)
    assert len(V) > 0
    time_col = auto_time_col(columns)

# what a hack...

    # - - - - -
    # WEEKLY
    # - - - - -
    outputdir = join(plot_dir,node,'weekly')
    if not exists(outputdir):
        makedirs(outputdir)

    end = dt2ts(datetime.utcnow())
    begin = dt2ts(datetime.utcnow() - timedelta(hours=24*7))
    assert end > begin

    print(node + ', weekly')
    for var in V:
        try:
            p(node,var,time_col,begin,end,outputdir)
        except KeyboardInterrupt:
            break
        except:
            traceback.print_exc()

    # - - - - -
    # MONTHLY
    # - - - - -
    outputdir = join(plot_dir,node,'monthly')
    if not exists(outputdir):
        makedirs(outputdir)

    end = dt2ts(datetime.utcnow())
    begin = dt2ts(datetime.utcnow() - timedelta(hours=30*24*7))
    assert end > begin

    print(node + ', monthly')
    for var in V:
        try:
            p(node,var,time_col,begin,end,outputdir)
        except KeyboardInterrupt:
            break
        except:
            traceback.print_exc()

