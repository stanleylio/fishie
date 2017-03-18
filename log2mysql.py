# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2017
import zmq,sys,json,logging,traceback,time,math
import logging.handlers
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from datetime import datetime
from os.path import expanduser
sys.path.append(expanduser('~'))
from node.storage.storage2 import storage
from node.config.config_support import import_node_config
from node.parse_support import parse_message,pretty_print


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

#store = storage(user='root',passwd=open(expanduser('~/mysql_cred')).read().strip(),dbname='uhcm')
store = storage()

def taskSampler():
    try:
        socks = dict(poller.poll(1000))
        if zsocket in socks and zmq.POLLIN == socks[zsocket]:
            m = zsocket.recv()
            logger.debug(m)
            #m = zsocket.recv_string()
            d = parse_message(m)
            if d is None:
                logger.warning('Message from unrecognized source: ' + m)
                return
        
            d['ReceptionTime'] = time.time()
            print('= = = = = = = = = = = = = = =')
            pretty_print(d)

            for k in d.keys():
                if type(d[k]) is datetime:
                    assert False,'wut?!'
                try:
                    if math.isnan(d[k]):
                        d[k] = None
                except TypeError:
                    pass

            table = d['node']
            tmp = {k:d[k] for k in set(store.get_list_of_columns(table)) if k in d}
            store.insert(table,tmp)
    except:
        logger.exception(traceback.format_exc())
        logger.exception(m)

logger.info(__file__ + ' is ready')
LoopingCall(taskSampler).start(0.001)
reactor.run()
zsocket.close()
logger.info(__file__ + ' terminated')
