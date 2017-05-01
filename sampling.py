#!/usr/bin/python
#
# Relay incoming serial messages to local RabbitMQ exchange "uhcm"
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2017
import serial,os,traceback,time,sys,pika,socket
import logging,logging.handlers
from random import choice
from socket import gethostname
from os.path import expanduser
sys.path.append(expanduser('~'))
from node.config.config_support import import_node_config
from cred import cred


exchange = 'uhcm'
nodeid = socket.gethostname()
config = import_node_config()


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


def rabbit_init():
    credentials = pika.PlainCredentials(nodeid,cred['rabbitmq'])
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange,type='topic',durable=True)
    return connection,channel


logger.info(__name__ + ' starts')

def initports():
    sps = config.sampling_serial_ports
    if len(sps) <= 0:
        print('No serial port to use. Terminating.')
        exit()
    logging.info('Using serial ports: {}'.format(sps))
    
    sps = [serial.Serial(tmp[0],tmp[1],timeout=0.1) for tmp in sps]
    for port in sps:
        port.flushInput()
        port.flushOutput()
    return sps

sps = initports()
connection,channel = rabbit_init()

logger.info(__name__ + ' is ready')
while True:
    try:
        if sps is None:
            logging.info('serial port closed')
            sps = initports()
            logging.info('serial port reopened')
        line = choice([port.readline() for port in sps]).strip()
        if len(line) > 0:
            print(line)
            if connection is None or channel is None:
                logging.info('Connection to local exchange closed')
                connection,channel = rabbit_init()
                logging.info('Connection to local exchange re-established')
            channel.basic_publish(exchange=exchange,
                                  routing_key=nodeid + '.samples',
                                  body=line,
                                  properties=pika.BasicProperties(delivery_mode=2,
                                                                  content_type='text/plain',
                                                                  expiration=str(72*3600*1000),
                                                                  timestamp=time.time()))
    except KeyboardInterrupt:
        logger.info('user interrupted')
        break
    except pika.exceptions.ConnectionClosed:
        connection,channel = None,None
        logging.error('connection closed')  # connection to the local exchange closed? wut?
        time.sleep(1)
    except serial.SerialException:
        logger.warning('USB-to-serial converters are EVIL')
        logging.warning(traceback.format_exc())
        sps = None
    except:
        logger.exception('Error processing: ' + line)
        logger.warning(format_exc())

connection.close()
for port in sps:
    port.close()
logger.info(__name__ + ' terminated')
