# replace all out-of-bound samples with SQLite Null
# min and max may not both (or at all) defined for any variable (column)
import sys,sqlite3,argparse,traceback
sys.path.append('..')
from storage.storage import storage_read_only
from config.config_support import *


def PRINT(s):
    print(s)
    #pass


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,description='')
parser.add_argument('--dbfile',type=str,default=None,metavar='dbfile',help='Path to the database file')
parser.add_argument('--site',type=str,default='poh',metavar='site',help='Name of the site. {poh,msb228,coconut}')
args = parser.parse_args()

site = args.site
PRINT('Site: {}'.format(site))

dbfile = args.dbfile
if dbfile is None:
    print('--dbfile is not specified. Terminating.')
    sys.exit()

#dbfile = '/home/nuc/node/storage/sensor_data.db'

store = storage_read_only(dbfile)
#tables = store.get_list_of_tables()
nodes = get_list_of_nodes(site)


for node_id in nodes:
    print '- - -'
    print 'node: ', node_id

    convfs = {}
    mins = {}
    maxs = {}
    #tmp = importlib.import_module('config.{}'.format(table))
    tmp = import_node_config(site,node_id)
    for c in tmp.conf:
        #try:
        #    convfs[c['dbtag']] = c['convf']
        #except KeyError:
        #    convfs[c['dbtag']] = lambda (x): x
        try:
            mins[c['dbtag']] = c['min']
        except KeyError:
            mins[c['dbtag']] = float('inf')
        try:
            maxs[c['dbtag']] = c['max']
        except KeyError:
            mins[c['dbtag']] = float('-inf')
    #print convfs
    #print mins
    #print maxs

    cols = store.get_list_of_columns(node_id)
    conn = sqlite3.connect(dbfile,\
                           detect_types=sqlite3.PARSE_DECLTYPES |\
                           sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    for tag in cols:
        print '\t',tag
        try:
            c.execute('UPDATE {node} SET {tag}=? WHERE {tag}<?'.format(node=node_id.replace('-','_'),tag=tag),(None,mins[tag],))
        except KeyError:
            pass
        try:
            c.execute('UPDATE {node} SET {tag}=? WHERE {tag}>?'.format(node=node_id.replace('-','_'),tag=tag),(None,maxs[tag],))
        except KeyError:
            pass

    conn.commit()
    conn.close()

