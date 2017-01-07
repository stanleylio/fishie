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
from node.storage.storage2 import storage_read_only as store2
from node.storage.storage2 import auto_time_col,id2table
from node.config.config_support import get_list_of_nodes,get_list_of_disp_vars,get_description,get_unit,get_plot_range


logging.basicConfig(level=logging.DEBUG)


def is_node(device):
    return not device.startswith('base-')


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


store = store2()
list_of_nodes = get_list_of_nodes(site)
for node in list_of_nodes:
    if not is_node(node):   # could be a base station or other stuff in the future
        continue

    # auto-select a column as time
    #V = get_list_of_disp_vars(site,node)
    V = get_list_of_disp_vars(node)
    columns = store.get_list_of_columns(id2table(node))
    assert set(V) <= set(columns)
    time_col = auto_time_col(columns)

    # create the output dir
    tmp = join(plot_dir,node)
    if not exists(tmp):
        makedirs(tmp)

    end = dt2ts(datetime.utcnow())
    begin = dt2ts(datetime.utcnow() - timedelta(hours=get_plot_range(site,node)))

    print node
    for var in V:
        r = store.read_time_range(node,time_col,[time_col,var],begin,end)
        print '\t' + var
        if r is None or len(r[time_col]) <= 0:
            continue
        #var_description = get_description(site,node,var)
        var_description = get_description(node,var)
        title = '{} ({} of {})'.format(var_description,var,node)
        #unit = get_unit(site,node,var)
        unit = get_unit(node,var)
        if unit is None:
            ylabel = '(unitless)'
        else:
            ylabel = unit

        x = r[time_col]
        y = r[var]
        plot_time_series(x,y,\
                         join(plot_dir,node,var + '.png'),\
                         title=title,\
                         ylabel=ylabel,\
                         linelabel=var)

        plot_config = {'time_begin':min(x),
                       'time_end':max(x),
                       'plot_generated_at':dt2ts(),
                       'data_point_count':len(filter(lambda yy: yy is not None and not math.isnan(yy),y)),
                       'unit':unit,
                       'description':var_description}
        with open(join(plot_dir,node,var + '.json'),'w') as f:
            json.dump(plot_config,f,separators=(',',':'))

exit()













for node_id in nodes:
    print('- - - - -')
    print('Node: ' + node_id)

    if dbfile is None:
        logging.critical('dbfile not specified. Terminating')
        sys.exit()
        
    store = storage_read_only(dbfile=dbfile)
    node = import_node_config(site,node_id)

    tag_unit_map = get_unit_map(site,node_id)
    tag_desc_map = get_description_map(site,node_id)
    node_plot_dir = join(plot_dir,node_id)

    # time_col
    try:
        time_col = auto_time_col(store,node_id)
    except sqlite3.OperationalError:
        logging.warning('{} not in {}. Skipping this node'.format(node_id,dbfile))
        continue
        
    variables = [c['dbtag'] for c in node.conf if c['plot']]
    plotted = []
    for var in variables:
        timerange = timedelta(hours=node.plot_range)
        cols = [time_col,var]

        title = '{} ({} of {})'.format(tag_desc_map[var],var,node_id)
        plotfilename = join(node_plot_dir,'{}.png'.format(var))

        try:
            tmp = store.read_past_time_period(node_id,time_col,cols,timerange)

            # don't plot if:
            #   there's no data for the sensor in the specified range (e.g. sensor has been removed, logger is not working), or
            #   all samples are None (sensor read failed -> samples become None but still carries timestamps)
            if tmp is None or all([v is None for v in tmp[var]]):
                logging.warning('\tNo data for {} of {} in the selected range'.\
                      format(var,node_id))
                continue

            x = tmp[time_col]
            y = [l if l is not None else float('NaN') for l in tmp[var]]

            y = medfilt(y,5)

            if not exists(node_plot_dir):
                makedirs(node_plot_dir)

            print('\t{}'.format(var))
            tmp = tag_unit_map[var]
            if tmp is None:
                tmp = '(unitless)'
            plot_time_series(x,y,plotfilename,title,ylabel=tmp,linelabel=var)

            # save settings of plot to JSON file
            plot_config = {'time_begin':time.mktime(min(x).timetuple()),
                           'time_end':time.mktime(max(x).timetuple()),
                           'plot_generated_at':time.mktime(datetime.utcnow().timetuple()),
                           #'data_point_count':len(y),
                           'data_point_count':len(filter(lambda x: x is not None and not math.isnan(x),y)),
                           time_col:[dt2ts(t) for t in x],
                           var:[v if not math.isnan(v) else None for v in y],   # Javascript does NOT like NaN in JSON strings.
                           'unit':tag_unit_map[var],
                           'description':tag_desc_map[var]}

            # website helper (data attributes, per plot/var)
            with open(join(node_plot_dir,var + '_withpt.json'),'w') as f:
                # json.dump vs. json.dumps...
                json.dump(plot_config,f,separators=(',',':'))

            plot_config.pop(time_col,None)
            plot_config.pop(var,None)
            with open(join(node_plot_dir,var + '.json'),'w') as f:
                # json.dump vs. json.dumps...
                json.dump(plot_config,f,separators=(',',':'))

            plotted.append(var)

        #except (sqlite3.OperationalError,ValueError) as e:
            # TypeError: ... I don't remember.
            # sqlite3.OperationalError: db is empty
            # ValueError: db has the variable, but all NaN
            #logging.warning('\tNo data for {} of {} in the selected range'.\
            #      format(var,node_id))
            #traceback.print_exc()
        except KeyboardInterrupt:
            logging.info('user interrupted')
            sys.exit()
        except:
            #traceback.print_exc()
            logging.error(traceback.format_exc())

    # website helper (list of variable, per node)
    if exists(node_plot_dir) and len(plotted) > 0:
        with open(join(node_plot_dir,'var_list.json'),'w') as f:
            #tmp = [v + '.png' for v in plotted]
            #json.dump({'variables':tmp},f,separators=(',',':'))
            json.dump({'variables':plotted},f,separators=(',',':'))

