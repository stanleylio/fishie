# generate static plots for the given site
# data are drawn from mysql db instead of sqlite
#
# Stanley H.I. Lio
# hlio@soest.hawaii.edu
# All Rights Reserved. 2016
import sys,traceback,json,time,math,logging,argparse
from os import makedirs
from os.path import exists,join,expanduser
sys.path.append(expanduser('~'))
from datetime import datetime,timedelta
#from scipy.signal import medfilt
from node.display.gen_plot import plot_time_series
from node.helper import dt2ts
from node.storage.storage2 import storage,auto_time_col
from node.config.config_support import get_list_of_devices,get_list_of_disp_vars,get_description,get_unit,get_plot_range


logging.basicConfig(level=logging.DEBUG)


def is_node(device):
    return not device.startswith('base-')

def find_bounds(x,y):
    '''Find both the oldest and the latest timestamp where the reading is not None'''
    tmp = filter(lambda p: p[1] is not None,zip(x,y))
    return min(tmp,key=lambda p: p[0])[0],max(tmp,key=lambda p: p[0])[0],


# db could be empty
# node may not be defined
# variable may not be defined
# there may not be any data for the variable
# there may not be any recent data for the variable
# the data could be None or NaN
# ...


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
#list_of_nodes = get_list_of_nodes(site)
list_of_nodes = get_list_of_devices(site)
for node in list_of_nodes:
#for node in ['node-025']:
    #if not is_node(node):   # could be a base station or other stuff in the future
    #    continue

    # auto-select a column as time
    #V = get_list_of_disp_vars(site,node)
    logging.info(node)
    V = get_list_of_disp_vars(node)
    try:
        columns = store.get_list_of_columns(node)
    except:
        traceback.print_exc()
        continue
    assert set(V) <= set(columns)
    assert len(V) > 0
    time_col = auto_time_col(columns)

    # create the output dir
    tmp = join(plot_dir,node)
    if not exists(tmp):
        makedirs(tmp)

    end = dt2ts(datetime.utcnow())
    begin = dt2ts(datetime.utcnow() - timedelta(hours=get_plot_range(node)))
    assert end > begin

    #print(node)

    for var in V:
        #print(var)
        #continue
        try:
            r = store.read_time_range(node,time_col,[time_col,var],begin,end)
            print('\t' + var)
            #if r is None or len(r[time_col]) <= 0: # should proceed even if it's an empty plot though. TODO
            if r is None or len(r[time_col]) <= 0 or all([tmp is None for tmp in r[var]]):
                logging.info('No data')
                continue
            var_description = get_description(node,var)
            title = '{} ({} of {})'.format(var_description,var,node)
            unit = get_unit(node,var)
            if unit is None:
                ylabel = '(unitless)'
            else:
                ylabel = unit

            # - - -
            x = r[time_col]
            y = r[var]
            plot_time_series(x,y,\
                             join(plot_dir,node,var + '.png'),\
                             title=title,\
                             ylabel=ylabel,\
                             linelabel=var)

            # this sounds like a classic SQL job.
            tmp = find_bounds(x,y)
            plot_config = {'time_begin':tmp[0],
                           'time_end':tmp[1],
                           'plot_generated_at':dt2ts(),
                           'data_point_count':len(filter(lambda yy: yy is not None and not math.isnan(yy),y)),
                           'unit':unit,
                           'description':var_description}
            with open(join(plot_dir,node,var + '.json'),'w') as f:
                json.dump(plot_config,f,separators=(',',':'))
        except OverflowError:
            traceback.print_exc()
