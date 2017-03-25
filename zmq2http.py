# relay xbee msgs (from zmq 9002) to HTTP POST v4 API
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2017
import zmq,sys,json,logging,traceback,time,socket,requests
import logging.handlers
from os.path import join,exists,expanduser
sys.path.append(expanduser('~'))
from datetime import datetime,timedelta
from node.config.config_support import import_node_config
#from uhcmrt_cred import cred
from node.send2server import post4


config = import_node_config()
node = socket.gethostname()

#url = config.zmq2http_url
#assert 1 == len(cred.keys())
#username = cred.keys()[0]


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


def send(d):
    try:
        m = json.dumps([node,d],separators=(',',':'))
        #r = requests.post(url,
        #                  data={'m':m},
        #                  auth=(username,cred[username]))
        #logger.debug(r)
        logger.debug(post4(m,'https://grogdata.soest.hawaii.edu/api/4'))
        send.last_transmitted = datetime.utcnow()
    except:
        logger.error(traceback.format_exc())
send.last_transmitted = datetime.utcnow()


logger.info(__file__ + ' is ready')
while True:
    try:
        socks = dict(poller.poll(1000))
        if zsocket in socks and zmq.POLLIN == socks[zsocket]:
            m = zsocket.recv()
            logger.debug(m)
            send(m)
        if datetime.utcnow() - send.last_transmitted > timedelta(minutes=5):
            send('')
    except KeyboardInterrupt:
        logger.info('user interrupted')
        break
    except:
        logger.exception(traceback.format_exc())
        logger.exception(m)

zsocket.close()
logger.info(__file__ + ' terminated')
