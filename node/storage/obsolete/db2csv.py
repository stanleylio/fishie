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
    desc_str = '''Dump the content of the database to a CSV. Example:
\tpython db2csv.py'''
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,description=desc_str)
    parser.add_argument('--last',type=int,metavar='last',help='the number of (latest) records to retrieve')
    args = parser.parse_args()
    last = args.last

    parser = SafeConfigParser()
    parser.read(join(dirname(__file__),'../node_config.ini'))   # patchy...
    tag = parser.get('storage','tag').split(',')
    #print tag

    print 'from sensor_data.db...'

    store = storage()
    if last is None:
        print 'reading entire database... (to get only the last N entries, use the --last switch)'
        tmp = store.read_all(tag)
    else:
        print 'reading last {} records...'.format(last)
        tmp = store.read_latest(count=last)

    print 'writing to file...'
    with open('sensor_data.csv','w',0) as f:

        f.write(','.join(tag) + '\n')

        for r in zip(*tmp):
            #print r[0].strftime('%Y-%m-%d %H:%M:%S')
            ts = time.mktime(r[0].timetuple())
            tmp = ','.join([str(v) for v in [ts] + list(r[1:])])
            #print tmp
            f.write(tmp + '\n')
            
    print 'done. see sensor_data.csv'
