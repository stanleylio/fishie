#!/usr/bin/python
#
# Relay incoming serial messages to local RabbitMQ exchange "uhcm"
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2017
import serial,os,traceback,time,sys,pika,socket,argparse
import logging,logging.handlers
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from os.path import expanduser,exists
sys.path.append(expanduser('~'))
from cred import cred
try:
    from node.drivers.watchdog import reset_auto
    has_watchdog = True
except:
    has_watchdog = False


exchange = 'uhcm'
nodeid = socket.gethostname()
reconnection_delay = 5


# I wonder if I could just get rid of this and let supervisor handle logging.
#'DEBUG,INFO,WARNING,ERROR,CRITICAL'
logging.basicConfig(level=logging.INFO)
logging.getLogger('pika').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address='/dev/log')
logging.Formatter.converter = time.gmtime
formatter = logging.Formatter('%(asctime)s,%(name)s,%(levelname)s,%(module)s.%(funcName)s,%(message)s')
#formatter = logging.Formatter('%(name)s,%(levelname)s,%(module)s.%(funcName)s,%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.debug('has_watchdog: {}'.format(has_watchdog))

parser = argparse.ArgumentParser(description='sampling.py')
parser.add_argument('port',metavar='serialport',type=str,
                    help='Path to the serial port')
parser.add_argument('baud',default=115200,type=int,
                    help='Baud rate to use')
args = parser.parse_args()


def rabbit_init():
    credentials = pika.PlainCredentials(nodeid,cred['rabbitmq'])
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange,exchange_type='topic',durable=True)
    return connection,channel


logger.info(__name__ + ' starts')

def initport():
    if not exists(args.port):
        print('Serial port {} not found. Terminating.'.format(args.port))
        exit()
    logger.info('Using serial ports {} at {}'.format(args.port,args.baud))
    
    port = serial.Serial(args.port,args.baud,timeout=0.5)
    port.flushInput()
    port.flushOutput()
    return port



def taskSampling():
    global port,connection,channel
    
    try:
        if port is None:
            logger.info('serial port not open')
            port = initport()
            logger.info('serial port reopened')
        
        line = port.readline()
        if len(line.strip()) > 0:
            print(line.strip())
            if connection is None or channel is None:
                logger.info('Connection to local exchange not open')
                connection,channel = rabbit_init()
                logger.info('Connection to local exchange re-established')
            channel.basic_publish(exchange=exchange,
                                  routing_key=nodeid + '.samples',
                                  body=line,
                                  properties=pika.BasicProperties(delivery_mode=2,
                                                                  content_type='text/plain',
                                                                  expiration=str(10*24*3600*1000)))
    except pika.exceptions.ConnectionClosed:
        logger.error('connection closed')  # connection to the local exchange closed? wut?
        connection,channel = None,None
        time.sleep(reconnection_delay)
    except serial.SerialException:
        logger.warning('USB-to-serial converters are EVIL')
        logger.warning(traceback.format_exc())
        port = None
    except:
        logger.exception('Error processing: ' + line)
        logger.warning(traceback.format_exc())


def taskWatchdog():
    try:
        reset_auto()
        logger.debug('watchdog reset')
    except:
        pass


port = None
connection,channel = None,None


logger.info(__name__ + ' is ready')
LoopingCall(taskSampling).start(0.001)
if has_watchdog:
    LoopingCall(taskWatchdog).start(2*60)

reactor.run()

if port is not None:
    port.close()
if connection is not None:
    connection.close()
logger.info(__name__ + ' terminated')
