"""
Relay incoming serial messages to a RabbitMQ exchange.

Remember that delivery_mode==2 increases flash memory wear. Don't use
that if you're not using eMMC, or if the SD card is small. If you're on
a Pi you could try the overlay filesystem, but that's basically
delivery_mode==1.

You might end up needing the overlay filesystem anyway because of
random, frequent power outages in the field.

Stanley H.I. Lio
"""
import logging, serial, os, time, sys, pika, socket, argparse, asyncio
import logging.handlers
from os.path import exists
from helper import init_rabbit
from cred import cred
try:
    from node.drivers.watchdog import reset_auto
    has_watchdog = True
except:
    has_watchdog = False


reconnection_delay_second = 11
watchdog_reset_second = 59
exchange = 'uhcm'
nodeid = socket.gethostname()


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

logger.debug(f'has_watchdog: {has_watchdog}')

parser = argparse.ArgumentParser(description='sampling2.py')
parser.add_argument('--port', metavar='serialport', type=str,
                    help='Path to the XBee serial port')
parser.add_argument('--baud', default=115200, type=int,
                    help='Baud rate to use')
parser.add_argument('--brokerip', metavar='broker', type=str,
                    help='Broker IP', default='localhost')
parser.add_argument('--brokerport', metavar='port', type=int,
                    help='Broker port', default=5672)
args = parser.parse_args()


logger.info(__name__ + ' starts')


should_continue = True

def init_serial_port():
    if not exists(args.port):
        logger.error(f'Serial port {args.port} not found. Terminating.')
        sys.exit()
    logger.info(f'Using serial port {args.port} at {args.baud}.')
    
    return serial.Serial(args.port, args.baud, timeout=0.5)


async def taskSampling():
    global port, connection, channel, should_continue

    while should_continue:
        try:
            if port is None:
                logger.info('serial port is not open.')
                port = init_serial_port()
                logger.info('serial port reopened')
            
            line = port.readline().strip()
            if len(line) > 0:
                logger.info(line)
                
                if connection is None or channel is None:
                    logger.info('Connection to local exchange is not open.')
                    connection, channel = init_rabbit(nodeid, cred['rabbitmq'], host=args.brokerip)
                    logger.info('Connection to local exchange re-established.')

                channel.basic_publish(exchange=exchange,
                                      routing_key=nodeid + '.s',
                                      body=line,
                                      properties=pika.BasicProperties(delivery_mode=2,
                                                                      content_type='text/plain',
                                                                      expiration=str(10*24*3600*1000)))
        except pika.exceptions.ConnectionClosed:
            logger.error('connection closed')  # connection to the local exchange closed? wut?
            
            connection, channel = None, None
            await asyncio.sleep(reconnection_delay_second)
            
        except serial.SerialException:

            logger.warning('USB-to-serial converters are EVIL')
            port = None

        except KeyboardInterrupt:
            raise
        
        except:
            logger.exception('Error processing: ' + line)

        await asyncio.sleep(0.005)


async def taskWatchdog():
    global should_continue
    
    while has_watchdog and should_continue:
        try:
            reset_auto()
            logger.debug('watchdog reset')
            
        except KeyboardInterrupt:
            raise
        
        except:
            logger.debug('no WDT?')
        
        await asyncio.sleep(watchdog_reset_second)


port = None
connection, channel = None, None

logger.info(__name__ + ' is ready')

try:
    asyncio.get_event_loop().run_until_complete(
        asyncio.gather(
            taskSampling(),
            taskWatchdog(),
            ))
except KeyboardInterrupt:
    should_continue = False
    logger.info('user interrupted')

if port is not None:
    port.close()
if connection is not None:
    connection.close()

logger.info(__name__ + ' terminated')
