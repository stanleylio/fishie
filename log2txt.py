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
from node.helper import dt2ts
from node.config.config_support import import_node_config


config = import_node_config()


# product of this script, the raw text file
output_path = getattr(config,'log2txt_output_path',None)
assert output_path is not None and exists(output_path)


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
topic = u''
context = zmq.Context()
zsocket = context.socket(zmq.SUB)
# Still not foolproof. Imagine power to both publisher and subscriber got cycled.
# publisher may come up after subscriber. This script should not proceed if
# no publisher is found. The static config is still needed.
# Also, how often should subscribers initiate a new search?
#a = set(config.subscribeto)         # feeds found in config
a = set(getattr(config,'subscribeto',[]))
b = set(get_publisher_list(topic))  # feeds found in the network
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
with open(join(output_path,'raw.txt'),'a',0) as raw,\
     open(join(output_path,'tsraw.txt'),'a',0) as tsraw:
    while True:
        try:
            socks = dict(poller.poll(1000))
            if zsocket in socks and zmq.POLLIN == socks[zsocket]:
                m = zsocket.recv()
                print('= = = = = = = = = =')
                print(m)
                
                raw.write(m)
                dt = datetime.utcnow()
                tsraw.write('{}\t{:6f}\t{}\n'.format(dt.isoformat(),dt2ts(dt),m.strip()))

                raw.flush()
                tsraw.flush()
                
        except KeyboardInterrupt:
            logger.info('user interrupted')
            break
        except:
            logger.warning(traceback.format_exc())
            logger.warning(m)

zsocket.close()
logger.info(__file__ + ' terminated')
