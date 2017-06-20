#!/usr/bin/python
#
# Relay incoming serial messages to local RabbitMQ exchange "uhcm"
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2017
import serial,os,traceback,time,sys,pika,socket,argparse
import logging,logging.handlers
from os.path import expanduser,exists
sys.path.append(expanduser('~'))
from cred import cred


exchange = 'uhcm'
nodeid = socket.gethostname()


# I wonder if I could just get rid of this and let supervisor handle logging.
#'DEBUG,INFO,WARNING,ERROR,CRITICAL'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address='/dev/log')
logging.Formatter.converter = time.gmtime
formatter = logging.Formatter('%(asctime)s,%(name)s,%(levelname)s,%(module)s.%(funcName)s,%(message)s')
#formatter = logging.Formatter('%(name)s,%(levelname)s,%(module)s.%(funcName)s,%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


parser = argparse.ArgumentParser(description='sampling.py')
parser.add_argument('port',metavar='serialport',type=str,
                    help='Path to the serial port')
parser.add_argument('baud',default=115200,type=int,
                    help='Baud rate to use')
args = parser.parse_args()


def rabbit_init():
    credentials = pika.PlainCredentials('nuc',cred['rabbitmq'])
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange,type='topic',durable=True)
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

port = initport()
connection,channel = rabbit_init()

logger.info(__name__ + ' is ready')
while True:
    try:
        if port is None:
            logger.info('serial port closed')
            port = initport()
            logger.info('serial port reopened')
        
        line = port.readline()
        if len(line.strip()) > 0:
            print(line.strip())
            if connection is None or channel is None:
                logger.info('Connection to local exchange closed')
                connection,channel = rabbit_init()
                logger.info('Connection to local exchange re-established')
            channel.basic_publish(exchange=exchange,
                                  routing_key=nodeid + '.samples',
                                  body=line,
                                  properties=pika.BasicProperties(delivery_mode=2,
                                                                  content_type='text/plain',
                                                                  expiration=str(30*24*3600*1000),
                                                                  timestamp=time.time()))
    except KeyboardInterrupt:
        logger.info('user interrupted')
        break
    except pika.exceptions.ConnectionClosed:
        logging.error('connection closed')  # connection to the local exchange closed? wut?
        connection,channel = None,None
        time.sleep(1)
    except serial.SerialException:
        logger.warning('USB-to-serial converters are EVIL')
        logger.warning(traceback.format_exc())
        sps = None
    except:
        logger.exception('Error processing: ' + line)
        logger.warning(traceback.format_exc())

connection.close()
port.close()
logger.info(__name__ + ' terminated')
