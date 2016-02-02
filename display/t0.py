# generate plots for debug webpage
#
# Stanley Lio, hlio@soest.hawaii.edu
# January 2016
import sys,traceback,sqlite3,re,importlib,argparse,json,time,math
sys.path.append('..')
from config.config_support import *
from storage.storage import storage_read_only,auto_time_col
from gen_plot import plot_multi_time_series,plot_time_series
from helper import dt2ts
from datetime import datetime,timedelta
from os.path import exists,join
from os import makedirs
#from scipy.signal import medfilt


def PRINT(s):
    print(s)
    #pass


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,description='')
parser.add_argument('--dbfile',type=str,default=None,metavar='dbfile',help='Path to the database file')
parser.add_argument('--site',type=str,default='poh',metavar='site',help='Name of the site. {poh,msb228,coconut}')
parser.add_argument('--plot_dir',type=str,default='./gen_plot_output',metavar='plot_dir',help='Output directory for the plots')
args = parser.parse_args()

site = args.site
PRINT('Site: {}'.format(site))

dbfile = args.dbfile
if dbfile is not None:
    PRINT('db: {}'.format(dbfile))

# which database to take data from
#dbfile = args.dbfile
#if not exists(dbfile):
#    print('dbfile {} not found. Terminating.'.format(dbfile))
#    sys.exit()
#else:
#    PRINT('Plotting data from {}'.format(dbfile))

# where to put the generated plots
plot_dir = args.plot_dir
PRINT('Output directory: ' + plot_dir)

#tmp = store.get_list_of_tables()
#nodes = [t.replace('_','-') for t in tmp if re.match('^node.+',t)]
nodes = get_list_of_nodes(site)

if len(nodes) <= 0:
    print('Nothing to plot. Terminating.')
    sys.exit()

# list of nodes, per site
with open(join(plot_dir,'node_list.json'),'w') as f:
    json.dump({'nodes':nodes},f,separators=(',',':'))

for node_id in nodes:
    PRINT('- - - - -')
    PRINT('Node: ' + node_id)

    if dbfile is None:
        print('dbfile not specified. Terminating')
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
        PRINT('{} not in {}. Skipping this node'.format(node_id,dbfile))
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
                           'data_point_count':len(y),
                           time_col:[dt2ts(t) for t in x],
                           var:[v if not math.isnan(v) else None for v in y],   # Javascript does NOT like NaN in JSON strings.
                           'unit':tag_unit_map[var],
                           'description':tag_desc_map[var]}

            # website helper (data attributes, per plot/var)
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
            traceback.print_exc()
        except:
            traceback.print_exc()

    # website helper (list of variable, per node)
    if exists(node_plot_dir) and len(plotted) > 0:
        with open(join(node_plot_dir,'var_list.json'),'w') as f:
            #tmp = [v + '.png' for v in plotted]
            #json.dump({'variables':tmp},f,separators=(',',':'))
            json.dump({'variables':plotted},f,separators=(',',':'))

