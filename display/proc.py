# replace all out-of-bound samples with SQLite Null
# min and max may not both (or at all) defined for any variable (column)
import sys,sqlite3,importlib,argparse,traceback
sys.path.append('..')
from storage.storage import storage_read_only


def PRINT(s):
    print(s)
    #pass


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,description='')
parser.add_argument('--dbfile',type=str,default=None,metavar='dbfile',help='Path to the database file')
args = parser.parse_args()

dbfile = args.dbfile
if dbfile is None:
    print('--dbfile is not specified. Terminating.')
    sys.exit()

#dbfile = '/home/nuc/node/storage/sensor_data.db'

store = storage_read_only(dbfile)
tables = store.get_list_of_tables()
#print tables
#exit()

for table in tables:
    print '- - -'
    print table

    convfs = {}
    mins = {}
    maxs = {}
    tmp = importlib.import_module('config.{}'.format(table))
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

    cols = store.get_list_of_columns(table)
    conn = sqlite3.connect(dbfile,\
                           detect_types=sqlite3.PARSE_DECLTYPES |\
                           sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    for tag in cols:
        print '\t',tag
        try:
            c.execute('UPDATE {table} SET {tag}=? WHERE {tag}<?'.format(table=table,tag=tag),(None,mins[tag],))
        except KeyError:
            pass
        try:
            c.execute('UPDATE {table} SET {tag}=? WHERE {tag}>?'.format(table=table,tag=tag),(None,maxs[tag],))
        except KeyError:
            pass

    conn.commit()
    conn.close()

