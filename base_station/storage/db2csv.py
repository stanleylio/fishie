from storage import storage
from ConfigParser import SafeConfigParser,NoSectionError
from os.path import join,dirname
from datetime import datetime
import time
import argparse

# dump the database into a CSV file
# timestamps are in POSIX floats (not human readable strings)
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

if '__main__' == __name__:
    desc_str = '''Dump the content of the database to CSVs. Example:
\tpython db2csv.py'''
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,description=desc_str)
    parser.add_argument('--node_id',type=int,metavar='NODE_ID',help='ID of the node')
    parser.add_argument('--last',type=int,metavar='last',help='the number of (latest) records to retrieve')
    args = parser.parse_args()
    last = args.last
    node_id = args.node_id

    if node_id is None:
        print 'ID of the node must be specified. Example: python db2csv.py --node_id 4'
        exit()

    parser = SafeConfigParser()
    parser.read(join(dirname(__file__),'../node_config.ini'))   # patchy...
    dbtag = parser.get('node_{:03d}'.format(node_id),'dbtag').split(',')

    print 'From sensor_data.db reading node_{:03d}...'.format(node_id)

    store = storage()
    if last is None:
        print 'Reading entire database... (to get only the last N entries, use the --last switch)'
        tmp = store.read_all(node_id,dbtag)
    else:
        print 'Reading last {} records...'.format(last)
        tmp = store.read_latest(node_id,count=last)

    print 'Writing to file...'
    with open('sensor_data_node_{:03d}.csv'.format(node_id),'w',0) as f:
        f.write(','.join(dbtag) + '\n')
        tmp = [tmp[t] for t in dbtag]
        for r in zip(*tmp):
            #print r[0].strftime('%Y-%m-%d %H:%M:%S')
            ts = time.mktime(r[0].timetuple())
            tmp = ','.join([str(v) for v in [ts] + list(r[1:])])
            #print tmp
            f.write(tmp + '\n')
            
    print 'done. see sensor_data.csv'
