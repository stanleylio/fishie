#!/usr/bin/python
#
# logging script for sensor node
#
# this one uses RabbitMQ
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2017
import serial,sys,time,traceback,logging,json,pika,socket
from os.path import join,exists,expanduser
sys.path.append(expanduser('~'))
import logging,logging.handlers
from datetime import datetime
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
#from random import random
from node.helper import dt2ts
from node.parse_support import pretty_print
from node.z import send,get_action
from node.drivers.indicators import *
from node.config.config_support import import_node_config
from cred import cred


exchange = 'uhcm'
nodeid = socket.gethostname()
config = import_node_config()

NGROUP = getattr(config,'NGROUP',1)
INTERVAL = getattr(config,'INTERVAL',60)
XBEE_PORT = getattr(config,'XBEE_PORT',None)
XBEE_BAUD = getattr(config,'XBEE_BAUD',115200)
XBEE_LOG_DIR = getattr(config,'XBEE_LOG_DIR',None)


#'DEBUG,INFO,WARNING,ERROR,CRITICAL'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address='/dev/log')
logging.Formatter.converter = time.gmtime
formatter = logging.Formatter('%(name)s,%(levelname)s,%(module)s.%(funcName)s,%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


from sampling_core import sampling_core


# hardware ports
if XBEE_PORT is None:
    logger.warning('XBEE_PORT not defined, no XBee telemetry!')
    xbeesend = lambda m: None
    ser = None
else:
    assert exists(XBEE_PORT)
    ser = serial.Serial(xbee_port,xbee_baud,timeout=1)
    xbeesend = lambda m: send(ser,m)

indicators_setup()

xbeesend({'status':'online',
          'INTERVAL':INTERVAL,
          'NGROUP':NGROUP,
          'Timestamp':time.time()})


def rabbit_init():
    credentials = pika.PlainCredentials(nodeid,cred['rabbitmq'])
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange,exchange_type='topic',durable=True)
    return connection,channel


if XBEE_LOG_DIR is None:
    XBEE_LOG_FILE = '/dev/null'
else:
    XBEE_LOG_FILE = join(config.XBEELOGDIR,'tsraw.txt')


# logging all incoming XBee traffic... just because.
rawf = open(XBEE_LOG_FILE,'a+',1)
def logtsraw(line):
    dt = datetime.utcnow()
    ts = dt2ts(dt)
    rawf.write('{}\t{}\t{}\n'.format(dt.isoformat(),ts,line.strip()))
    rawf.flush()


debt = 0
outqueue = []

def borrow(N=1):
    global debt
    assert debt >= 0
    if debt < 10*NGROUP:    # "debt ceiling"
        debt += N
        return True
    return False

def payback():
    global debt
    if debt > 0:
        debt -= 1
    assert debt >= 0


connection,channel = rabbit_init()
def taskSampling():
    try:
        if debt <= 0:
            return
        
        red_on()
        usr0_on()

        d = sampling_core()
        if len(d) <= 0:
            print('sampling_core() returns nothing')
            return
        
        print('= = = = = = = = = =')
        pretty_print(d)

        #tmp = {c.get('comtag',c['dbtag']):d[c['dbtag']] for c in config.conf}
        #outqueue.append(tmp)
        outqueue.append(d)

        # This turns the "local" sample (a dict) into a message that base
        # stations expect. This way the base station's log2mysql.py can
        # be reused.
        # In the future these bbb nodes should ALL double as base stations,
        # listening and parsing all messages in the air.

        m = send(None,d,src=nodeid)
        #socket.send(m)

        global channel,connection
        if connection is None or channel is None:
            connection,channel = rabbit_init()
        channel.basic_publish(exchange=exchange,
                              routing_key=nodeid + '.samples',
                              body=m,
                              properties=pika.BasicProperties(delivery_mode=2,
                                                              content_type='text/plain',
                                                              expiration=str(72*3600*1000)))

        red_off()
        usr0_off()

        payback()
        if debt > 0:
            logger.debug('debt={}'.format(debt))
            #reactor.callLater(2*random(),taskSampling)
        else:
            logger.debug('all debts are paid')
    except pika.exceptions.ConnectionClosed:
        connection,channel = None,None
        logging.error('connection closed')  # connection to the local exchange closed? wut?
    except:
        logger.error(traceback.format_exc())

def taskTrigger():
    try:
        if not borrow(NGROUP):
            logging.warning('ran out of credit')
        #reactor.callLater(0,taskSampling)
    except:
        logger.error(traceback.format_exc())

def taskSerial():
    try:
        line = ser.readline()
        if len(line) > 0:
            logtsraw(line)

            cmd = get_action(line)
            if cmd is not None and ('do sample' == cmd['action']):
                logger.debug('cmd: do sample')
                borrow(1)
                #reactor.callLater(0,taskSampling)

        if len(outqueue):
            xbeesend(outqueue.pop(0))
    except:
        logger.error(traceback.format_exc())

def taskBlink():
    usr3_on()
    green_on()
    time.sleep(0.05)
    usr3_off()
    green_off()

LoopingCall(taskSampling).start(0.1)
LoopingCall(taskTrigger).start(INTERVAL)
if ser is not None:
    LoopingCall(taskSerial).start(0.05,now=False)
LoopingCall(taskBlink).start(1)

logger.info(__name__ + ' is ready')
reactor.run()

connection.close()
if ser is not None:
    ser.close()
rawf.close()
indicators_cleanup()
logger.info(__name__ + ' terminated')
