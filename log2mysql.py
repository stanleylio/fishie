# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2017
import sys,traceback,time,math,MySQLdb,argparse,fileinput
from os.path import expanduser
sys.path.append(expanduser('~'))
from node.parse_support import parse_message,pretty_print
from node.storage.storage2 import storage


parser = argparse.ArgumentParser(description="""Read node messages from STDIN and write to MySQL db.
Example: python log2mysql.py""")
args,unk = parser.parse_known_args()


def init_storage():
    return storage()
store = init_storage()


def callback(m):
    global store
    try:
        d = parse_message(m)
        if d is None:
            print('Message from unrecognized source: ' + m)
            return

        d['ReceptionTime'] = time.time()
        print('= = = = = = = = = = = = = = =')
        pretty_print(d)

        for k in d.keys():
            try:
                if math.isnan(d[k]):
                    d[k] = None
            except TypeError:
                pass

        table = d['node']
        tmp = {k:d[k] for k in store.get_list_of_columns(table) if k in d}
        store.insert(table,tmp)
    except MySQLdb.OperationalError,e:
        store = init_storage()
    except:
        traceback.print_exc()
        print(m)


for line in fileinput.input(unk):
    callback(line)
