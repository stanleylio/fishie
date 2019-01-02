# Generate static plots for a given site
#
# Stanley H.I. Lio
import sys, traceback, json, time, math, logging, argparse, pytz
from os import makedirs
from os.path import exists, join, expanduser
sys.path.append(expanduser('~'))
from datetime import datetime, timedelta
#from scipy.signal import medfilt
from node.display.gen_plot import plot_time_series
from node.helper import ts2dt, dt2ts
from node.storage.storage2 import storage, auto_time_col
from node.config.config_support import get_list_of_sites, get_list_of_devices, get_list_of_disp_vars, get_description, get_unit, get_config

from skyfield import api
load = api.Loader('~/skyfield-data', verbose=False)
timescale = load.timescale()
planets = load('de421.bsp')
from skyfield import almanac

logging.basicConfig(level=logging.DEBUG)


#def is_node(device):
#    return not device.startswith('base-')

def find_bounds(x, y):
    '''Find both the oldest and the latest timestamp where the reading is not None'''
    tmp = list(filter(lambda p: p[1] is not None, zip(x, y)))
    return min(tmp, key=lambda p: p[0])[0], max(tmp, key=lambda p: p[0])[0],

def count_not_null(x, y):
    return len(list(filter(lambda p: p[1] is not None, zip(x, y))))


# db could be empty
# node may not be defined in db
# node may not be defined in config
# variable may not be defined in db
# variable may not be defined in config
# there may not be any data for the variable
# there may not be any recent data for the variable
# the reading could be None or NaN
# ...


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description='')
parser.add_argument('--site', type=str, metavar='site', help='Name of the site.')
parser.add_argument('--node', type=str, default=None, metavar='node', help='Name of a node.')
parser.add_argument('--var', type=str, default=None, metavar='var', help='Name of a variable.')

args = parser.parse_args()

# if var is specified, then site and node must also be specified.
# if node is specified, then site must also be specified.
# site can be given on its own.
if args.site:
    print('Site = {}'.format(args.site))
if args.node:
    print('node = {}'.format(args.node))
    assert args.site is not None
if args.var:
    print('var = {}'.format(args.var))
    assert args.node is not None and args.site is not None
root_plot_dir = '/var/www/uhcm/img'
print('Output dir = ' + root_plot_dir)
assert exists(root_plot_dir)

store = storage()

if args.site:
    sites = [args.site]
else:
    sites = get_list_of_sites()

for site in sites:

    print(site)
    
    plot_dir = join(root_plot_dir, site)
    if not exists(plot_dir):
        makedirs(plot_dir)

    if args.node:
        list_of_nodes = [args.node]
    else:
        list_of_nodes = get_list_of_devices(site)

    #assert len(list_of_nodes)

    query_end = dt2ts(datetime.utcnow())
    for node in list_of_nodes:

        print(node)

        # auto-select a column as time
        if args.var:
            list_variables = [args.var]
        else:
            list_variables = get_list_of_disp_vars(node)
        if len(list_variables) == 0:
            logging.warning('Nothing to plot for {}'.format(node))
            continue

        columns = store.get_list_of_columns(node)
        if len(columns) == 0:
            logging.warning('No table for {}'.format(node))
            continue

        assert set(list_variables) <= set(columns)
        time_col = auto_time_col(columns)

        latitude = get_config('latitude', node)
        longitude = get_config('longitude', node)
        #continue

        # create the output dir
        tmp = join(plot_dir, node)
        if not exists(tmp):
            makedirs(tmp)

        for var in list_variables:
            #print(var)
            #continue

            #if 'node-126' != node or 'd2w' != var:
            #    continue

            query_begin = dt2ts(datetime.utcnow() - timedelta(hours=get_config('plot_range', node, variable_name=var, default=30*24)))
            assert query_end > query_begin
            
            try:
                # ... sounds like a classic SQL job...
                r = store.read_time_range(node, time_col, [time_col, var], query_begin, query_end)
                print('\t' + var)
                #if r is None or len(r[time_col]) <= 0: # should proceed even if it's an empty plot though. TODO
                if r is None or len(r[time_col]) <= 0 or all([tmp is None for tmp in r[var]]):
                    logging.warning('No data for {}->{}'.format(node, var))
                    continue
                
                var_description = get_description(node,var)
                title = '{} ({} of {})'.format(var_description, var, node)
                unit = get_unit(node, var)
                if unit is None:
                    ylabel = '(unitless)'
                else:
                    ylabel = unit

                # - - -
                x = r[time_col]
                y = r[var]
                valid_begin, valid_end = min(x), max(x)
                if count_not_null(x, y):
                    valid_begin, valid_end = find_bounds(x, y)
                    if time.time() - valid_end > 24*3600:
                        color = '#9b9b9b'
                    else:
                        color = '#1f77b4'

                sun = None
                if latitude is not None and longitude is not None:
                    #print(latitude, longitude, valid_begin, valid_end)
                    tmp = api.Topos(latitude_degrees=latitude, longitude_degrees=longitude)
                    # epsilon is in unit of Julian days - down to the minute is fine.
                    risesettimes, isrise = almanac.find_discrete(timescale.utc(ts2dt(valid_begin).replace(tzinfo=pytz.utc)),
                                                 timescale.utc(ts2dt(valid_end).replace(tzinfo=pytz.utc)),
                                                 almanac.sunrise_sunset(planets, tmp),
                                                 epsilon=1/24/60)
                    #print(t.utc_iso())
                    sun = list(zip([tmp.utc_datetime() for tmp in risesettimes], isrise))
                #continue

                #print(color,time.time() - end,time.time() - max(x))
                plot_time_series(x,
                                 y,
                                 join(plot_dir, node, var + '.png'),
                                 sun=sun,
                                 title=title,
                                 ylabel=ylabel,
                                 linelabel=var,
                                 color=color,
                                 linestyle='',
                                 markersize=6)

                plot_config = {'time_begin':valid_begin,
                               'time_end':valid_end,
                               'plot_generated_at':dt2ts(),
                               'data_point_count':len(list(filter(lambda yy: yy is not None and not math.isnan(yy), y))),
                               'unit':unit,
                               'description':var_description}
                with open(join(plot_dir, node, var + '.json'), 'w') as f:
                    json.dump(plot_config, f, separators=(',', ':'))
            except (OverflowError, RuntimeError):
                traceback.print_exc()
