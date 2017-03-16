# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2016
import zmq,sys,json,logging,traceback,time,socket
import logging.handlers
from datetime import datetime,timedelta
from node.config.config_support import import_node_config


baseconfig = import_node_config()


#'DEBUG,INFO,WARNING,ERROR,CRITICAL'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address='/dev/log')
logging.Formatter.converter = time.gmtime
formatter = logging.Formatter('%(asctime)s,%(name)s,%(levelname)s,%(module)s.%(funcName)s,%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# ZMQ IPC stuff
topic = u''
context = zmq.Context()
zsocket = context.socket(zmq.SUB)
zsocket.connect('tcp://127.0.0.1:9002')
zsocket.setsockopt_string(zmq.SUBSCRIBE,topic)

poller = zmq.Poller()
poller.register(zsocket,zmq.POLLIN)


# communication
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


def send(d):
    try:
        s = json.dumps([node,d],separators=(',',':'))
        sock.sendto(s,('grog.soest.hawaii.edu',9007))
        send.last_transmitted = datetime.utcnow()
    except:
        logger.error(traceback.format_exc())
send.last_transmitted = datetime.utcnow()


logger.info(__file__ + ' is ready')
while True:
    try:
        socks = dict(poller.poll(100))
        if zsocket in socks and zmq.POLLIN == socks[zsocket]:
            m = zsocket.recv()
            print(m)
            send(m)
        if datetime.utcnow() - send.last_transmitted > timedelta(minutes=5):
            send('')
    except KeyboardInterrupt:
        logger.info('user interrupted')
        break
    except:
        logger.warning(traceback.format_exc())
        logger.warning(m)

zsocket.close()
logger.info(__file__ + ' terminated')
