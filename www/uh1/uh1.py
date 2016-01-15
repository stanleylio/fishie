#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015
import sys,traceback,sqlite3,importlib,argparse,numpy,traceback,re,json,time
sys.path.append('../..')
from datetime import datetime,timedelta
from config.config_support import *
from os.path import exists,join
from os import makedirs
from storage.storage import storage_read_only
from scipy.signal import medfilt


def PRINT(s):
    print(s)
    #pass


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,description='')
parser.add_argument('--dbfile',type=str,default='./sensor_data.db',metavar='dbfile',help='Path to the database file')
parser.add_argument('--out_dir',type=str,default='./uh1',metavar='out_dir',help='Output directory')

args = parser.parse_args()

# which database to take data from
dbfile = args.dbfile
if not exists(dbfile):
    print('dbfile {} not found. Terminating.'.format(dbfile))
    sys.exit()
else:
    print('Taking data from {}'.format(dbfile))

out_dir = args.out_dir
PRINT('Output directory: ' + out_dir)

store = storage_read_only(dbfile=dbfile)

tmp = store.get_list_of_tables()
nodes = [t.replace('_','-') for t in tmp if re.match('^node.+',t)]
for node_id in nodes:
    PRINT('- - - - -')
    PRINT('node ID:' + node_id)
    node = importlib.import_module('config.' + node_id.replace('-','_'))

    tag_unit_map = get_unit_map(node_id)
    tag_desc_map = get_description_map(node_id)
    node_out_dir = join(out_dir,node_id)

    # time_col
    time_col = None
    tmp = store.get_list_of_columns(node_id)
    if 'ReceptionTime' in tmp:
        time_col = 'ReceptionTime'
    elif 'Timestamp' in tmp:
        time_col = 'Timestamp'
    else:
        PRINT('uh1.py: no timestamp column found. Skipping this node.')
        continue

    variables = [c['dbtag'] for c in node.conf if c['plot']]
    # normally this should be redundant (database and config are consistent)
    tmp = store.get_list_of_columns(node_id)
    variables = [v for v in variables if v in tmp]
    plotted = []
    for var in variables:
        timerange = timedelta(hours=node.plot_range)
        cols = [time_col,var]

        try:
            tmp = store.read_past_time_period(node_id,time_col,cols,timerange)
            x = tmp[time_col]
            x = [time.mktime(t.timetuple()) for t in x]
            y = [l if l is not None else float('NaN') for l in tmp[var]]
            #y = medfilt(y,5)

            if not exists(node_out_dir):
                makedirs(node_out_dir)

            PRINT('\t{}'.format(var))
            with open(join(node_out_dir,'{}.json'.format(var)),'w') as f:
                json.dump({time_col:x,var:y},f,separators=(',',':'))

            plotted.append(var)
        except sqlite3.OperationalError:
            PRINT('No such var/node')
        except (TypeError,ValueError) as e:
            # TypeError: ... I don't remember.
            # sqlite3.OperationalError: db is empty
            # ValueError: db has the variable, but all NaN
            PRINT('\tNo data for {} of {} in the selected range'.\
                  format(var,node_id))
            #traceback.print_exc()
        except:
            traceback.print_exc()

    # website helper
    if exists(node_out_dir) and len(plotted) > 0:
        with open(join(node_out_dir,'var_list.json'),'w') as f:
            tmp = [v + '.png' for v in plotted]
            json.dump(tmp,f,separators=(',',':'))

