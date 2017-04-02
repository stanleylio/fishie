#!/usr/bin/python
#
# For base stations (NOT for nodes)
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2017
import serial,os,traceback,time,zmq,glob,sys
import logging,logging.handlers
from random import choice
from socket import gethostname
from os.path import expanduser
sys.path.append(expanduser('~'))
from node.config.config_support import import_node_config


#config = import_node_config()


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
zmq_port = 'tcp://127.0.0.1:9002'
context = zmq.Context()
zsocket = context.socket(zmq.PUB)
zsocket.bind(zmq_port)


logger.info(__name__ + ' starts')

def initports():
    sps = glob.glob('/dev/ttyUSB*')
    sps.extend(glob.glob('/dev/ttyO*'))
    if len(sps) <= 0:
        print('No serial port to use. Terminating.')
        exit()
    logging.info('Using serial ports: {}'.format(sps))
    
    sps = [serial.Serial(tmp,115200,timeout=0.1) for tmp in sps]

    for port in sps:
        port.flushInput()
        port.flushOutput()
    return sps

sps = initports()


logger.info(__name__ + ' is ready')
while True:
    try:
        line = choice([port.readline() for port in sps]).strip()
        if len(line) > 0:
            print(line)
            zsocket.send(line)
    except KeyboardInterrupt:
        logger.info('user interrupted')
        break
    except serial.SerialException:
        logger.warning('USB-to-serial converters are EVIL')
        logging.warning(traceback.format_exc())
        sps = initports()
    except:
        logger.exception('Error processing: ' + line)
        logger.warning(format_exc())

for port in sps:
    port.close()
zsocket.close()
logger.info(__name__ + ' terminated')
