# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2016
import sys,logging,traceback,socket
from os.path import expanduser
from datetime import datetime
sys.path.append(expanduser('~'))
from node.config.config_support import get_schema
from node.parse_support import parse_message,pretty_print
from node.storage.storage import storage
from node.config.config_support import import_node_config,get_site
from node.helper import ts2dt
from zmqloop import zmqloop


site = get_site(socket.gethostname())
config = import_node_config()


# init sqlite db
# add ReceptionTime
s = get_schema(site)
for k,v in s.iteritems():
    v.insert(0,('ReceptionTime','TIMESTAMP'))
store = storage(dbfile=config.dbfile,schema=s)


def callback(m):
    try:
        dt = datetime.utcnow()
        d = parse_message(m)

        if d is not None:
            # the old sqlite db still uses datetime instead of timestamps...
            # TODO: remove this!
            try:
                d['Timestamp'] = ts2dt(d['Timestamp'])
            except:
                pass
            d['ReceptionTime'] = dt
            print('= = = = = = = = = =')
            pretty_print(d)
            store.write(d)
        else:
            logger.warning('Message from unrecognized source: ' + m)
    except:
        traceback.print_exc()
        logging.exception(m)
    
zmqloop(callback)
