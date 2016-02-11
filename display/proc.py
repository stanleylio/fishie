# replace all out-of-bound samples with SQLite Null
# min and max may not both (or at all) defined for any variable (column)
#
# Stanley Lio, hlio@soest.hawaii.edu
# December 2015
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


for node in nodes:
    print '- - -'
    print 'node: ', node

    '''#convfs = {}
    mins = {}
    maxs = {}
    tmp = import_node_config(site,node)
    for c in tmp.conf:
        #try:
        #    convfs[c['db']] = c['convf']
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
    #print maxs'''

    cols = store.get_list_of_columns(node)
    conn = sqlite3.connect(dbfile,\
                           detect_types=sqlite3.PARSE_DECLTYPES |\
                           sqlite3.PARSE_COLNAMES)
    table = node.replace('-','_')
    
    c = conn.cursor()
    for variable in cols:
        r = get_range(site,node,variable)
        if r is None:
            PRINT('\tRange not defined for ({})'.format(' | '.join((site,node,variable))))
        else:
            print '\t',variable
            try:
                c.execute('UPDATE {table} SET {variable}=? WHERE {variable}<?'.\
                          format(table=table,variable=variable),(None,r['lb'],))
                c.execute('UPDATE {table} SET {variable}=? WHERE {variable}>?'.\
                          format(table=table,variable=variable),(None,r['ub'],))
            except:
                traceback.print_exc()

    conn.commit()
    conn.close()

