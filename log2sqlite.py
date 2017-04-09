# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2016
import sys,zmq,sys,json,logging,traceback,math,time,socket
import logging.handlers
from os.path import join,exists,expanduser
from datetime import datetime
sys.path.append(expanduser('~'))
from node.config.config_support import get_schema
from node.parse_support import parse_message,pretty_print
from node.storage.storage import storage
from node.config.config_support import import_node_config,get_site
from node.helper import ts2dt


site = get_site(socket.gethostname())
config = import_node_config()


#'DEBUG,INFO,WARNING,ERROR,CRITICAL'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address='/dev/log')
logging.Formatter.converter = time.gmtime
formatter = logging.Formatter('%(name)s,%(levelname)s,%(module)s.%(funcName)s,%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# ZMQ IPC stuff
topic = u''
context = zmq.Context()
zsocket = context.socket(zmq.SUB)
for feed in config.subscribeto:
    feed = 'tcp://' + feed
    logger.info('subscribing to ' + feed)
    zsocket.connect(feed)
zsocket.setsockopt_string(zmq.SUBSCRIBE,topic)
poller = zmq.Poller()
poller.register(zsocket,zmq.POLLIN)

# add ReceptionTime
s = get_schema(site)
for k,v in s.iteritems():
    v.insert(0,('ReceptionTime','TIMESTAMP'))


store = storage(dbfile=config.dbfile,schema=s)


logger.info(__file__ + ' is ready')
while True:
    try:
        socks = dict(poller.poll(1000))
        if zsocket in socks and zmq.POLLIN == socks[zsocket]:
            m = zsocket.recv()
            dt = datetime.utcnow()
            d = parse_message(m)

            # TODO: remove this!
            try:
                d['Timestamp'] = ts2dt(d['Timestamp'])   # the old sqlite db still uses datetime instead of timestamps...
            except:
                pass

            if d is not None:
                d['ReceptionTime'] = dt
                print('= = = = = = = = = =')
                pretty_print(d)
                store.write(d)
            else:
                logger.warning('Message from unrecognized source: ' + m)
    except KeyboardInterrupt:
        logger.info('user interrupted')
        break
    except:
        logger.warning(traceback.format_exc())
        logger.warning(m)

zsocket.close()
logger.info(__file__ + ' terminated')
