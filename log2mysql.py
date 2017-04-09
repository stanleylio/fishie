# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2017
import zmq,sys,json,traceback,time,math,MySQLdb
from os.path import expanduser
sys.path.append(expanduser('~'))
#from datetime import datetime
from node.zmqloop import zmqloop
from node.parse_support import parse_message,pretty_print
from node.storage.storage2 import storage
from cred import cred


def init_storage():
    #store = storage(user='root',passwd=open(expanduser('~/mysql_cred')).read().strip(),dbname='uhcm')
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
        store.insert(table,d)
    except MySQLdb.OperationalError,e:
        if e.args[0] in (MySQLdb.constants.CR.SERVER_GONE_ERROR,MySQLdb.constants.CR.SERVER_LOST):
            store = init_storage()
    except:
        traceback.print_exc()
        print(m)
    

zmqloop(callback)
