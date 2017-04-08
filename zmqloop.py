# store stuff from zmq to text file, with timestamps
# 
# Stanley H.I. Lio
# hlio@hawaii.edu
# University of Hawaii
# All Rights Reserved, 2017
import zmq,logging,time,sys,traceback
import logging.handlers
from os.path import exists,join,expanduser
sys.path.append(expanduser('~'))
from datetime import datetime
from node.config.config_support import import_node_config
from kmetlog.service_discovery import get_publisher_list


# I have doubt...
def zmqloop(callback,topic=u''):
    config = import_node_config()


    #'DEBUG,INFO,WARNING,ERROR,CRITICAL'
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.handlers.SysLogHandler(address='/dev/log')
    logging.Formatter.converter = time.gmtime
    #formatter = logging.Formatter('%(asctime)s,%(name)s,%(levelname)s,%(module)s.%(funcName)s,%(message)s')
    formatter = logging.Formatter('%(name)s,%(levelname)s,%(module)s.%(funcName)s,%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    # ZMQ IPC stuff
    #topic = u''
    context = zmq.Context()
    zsocket = context.socket(zmq.SUB)
    # Still not foolproof. Imagine power to both publisher and subscriber got cycled.
    # Subscriber may come up before publisher. This script should not proceed if no
    # publisher is found. The static config is still needed.
    # Also, how often should subscribers initiate a new search?
    # feeds found in config
    a = set(getattr(config,'subscribeto',[]))
    assert len(a) > 0 or len(topic) > 0,\
           'Either define some static endpoints in config file, or name at least one service to search for.'
    # feeds found in the network
    b = set(get_publisher_list(topic))
    feeds = a.union(b)
    assert len(feeds) > 0,'No ZMQ feed defined/found.'
    for feed in feeds:
        feed = 'tcp://' + feed
        logger.info('subscribing to ' + feed)
        zsocket.connect(feed)
    zsocket.setsockopt_string(zmq.SUBSCRIBE,topic)
    poller = zmq.Poller()
    poller.register(zsocket,zmq.POLLIN)

    logger.info(__file__ + ' is ready')

    while True:
        try:
            socks = dict(poller.poll(1000))
            if zsocket in socks and zmq.POLLIN == socks[zsocket]:
                m = zsocket.recv()
                #print('= = = = = = = = = =')
                #print(m)
                callback(m)
        except KeyboardInterrupt:
            logger.info('user interrupted')
            break
        except:
            logger.warning(traceback.format_exc())
            logger.warning(m)

    zsocket.close()
    logger.info(__file__ + ' terminated')
