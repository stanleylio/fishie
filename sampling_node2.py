"""

Stanley H.I. Lio
"""
import serial, sys, time, logging, json, pika, socket, argparse, asyncio
from os.path import join, exists, expanduser
sys.path.append(expanduser('~'))
import logging, logging.handlers
from datetime import datetime
from node.helper import dt2ts
from node.parse_support import pretty_print
from node.z import send, get_action
from cred import cred
from node.helper import is_rpi, init_rabbit


logging.getLogger('pika').setLevel(logging.WARNING)

exchange='uhcm'
nodeid = socket.gethostname()
routing_key = nodeid + '.s'

parser = argparse.ArgumentParser(description='ding')
parser.add_argument('--NGROUP', default=1, type=int, help='number of samples to take every period')
parser.add_argument('--INTERVAL', default=60, type=int, help='seconds to wait between group of samples')
parser.add_argument('--XBEE_PORT', default=None, type=str, help='serial port to XBee')
parser.add_argument('--XBEE_BAUD', default=115200, type=int, help='XBee baud rate')
parser.add_argument('--XBEE_LOG_DIR', default=None, type=str, help='where to store XBee traffic overheard')
parser.add_argument('--RABBITMQ_ENABLED', default=1, type=int, help='0: disabled; 1: enabled')
parser.add_argument('--SENDER_ID', default=nodeid, type=str)

args = parser.parse_args()

NGROUP = args.NGROUP
INTERVAL = args.INTERVAL
XBEE_PORT = args.XBEE_PORT
XBEE_BAUD = args.XBEE_BAUD
XBEE_LOG_DIR = args.XBEE_LOG_DIR
RABBITMQ_ENABLED = args.RABBITMQ_ENABLED
SENDER_ID = args.SENDER_ID


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
    logger.warning('XBEE_PORT not defined. No XBee telemetry!')
    xbeesend = lambda m: None
    ser = None
else:
    assert exists(XBEE_PORT)
    ser = serial.Serial(XBEE_PORT, XBEE_BAUD, timeout=1)
    xbeesend = lambda m: send(ser, m)

xbeesend({'status':'online',
          'INTERVAL':INTERVAL,
          'NGROUP':NGROUP,
          'ts':time.time()})


if XBEE_LOG_DIR is None:
    XBEE_LOG_FILE = '/dev/null'
else:
    XBEE_LOG_FILE = join(XBEE_LOG_DIR, 'tsraw.txt')


# logging all incoming XBee traffic... just because.
def logtsraw(line):
    dt = datetime.utcnow()
    ts = dt2ts(dt)
    rawf = open(XBEE_LOG_FILE, 'a+', 1)
    rawf.write('{}\t{}\t{}\n'.format(dt.isoformat(), ts,line.strip()))
    rawf.flush()


debt = 0
outqueue = []
should_continue = True
DEBT_CEILING = 10*NGROUP


def borrow(N):
    global debt

    logger.debug(f"debt {debt}; borrowing {N}")
    
    assert debt >= 0
    
    if debt + N <= DEBT_CEILING:
        debt += N
        return True
    return False


def payback():
    global debt

    logger.debug(f"debt={debt}")
    
    if debt > 0:
        debt -= 1
    assert debt >= 0


connection, channel = None, None
async def taskSampling():
    global should_continue, debt
    global connection, channel

    while should_continue:
        assert debt >= 0
        
        try:
            if debt > 0:
                logger.debug(f"owe {debt} sample(s)")
                
                if not is_rpi():
                    red_on()
                    usr0_on()

                d = sampling_core()
                if d is not None and len(d) > 0:
                    logger.debug(d)
                    
                    print('= = = = = = = = = =')
                    pretty_print(d)

                    outqueue.append(d)

                    m = send(None, d, src=SENDER_ID)

                    if RABBITMQ_ENABLED:
                        if connection is None or channel is None:
                            connection, channel = init_rabbit(nodeid, cred['rabbitmq'])
                        channel.basic_publish(exchange=exchange,
                                              routing_key=routing_key,
                                              body=m,
                                              properties=pika.BasicProperties(delivery_mode=2,
                                                                              content_type='text/plain',
                                                                              expiration=str(7*24*3600*1000)))

                    if not is_rpi():
                        red_off()
                        usr0_off()

                    payback()
                    
                else:
                    logger.info('sampling_core() returns nothing')
            else:
                logger.debug("Doesn't owe a sample.")

        except pika.exceptions.ConnectionClosed:
            connection, channel = None, None
            logger.error('connection closed')  # connection to the local exchange closed? wut?

        except KeyboardInterrupt:
            raise
        
        except:
            logger.exception('')
            #raise

        if debt > 0:
            await asyncio.sleep(INTERVAL/NGROUP/10)
        else:
            await asyncio.sleep(INTERVAL/NGROUP/2)
        

async def taskTrigger():
    global should_continue, debt
    
    while should_continue:
        try:
            if not borrow(NGROUP):
                logger.warning('ran out of credit')

        except KeyboardInterrupt:
            raise
        
        except:
            logger.exception('')

        await asyncio.sleep(INTERVAL)


async def taskSerial():
    global should_continue
    
    while should_continue:
        try:
            line = ser.readline()
            if len(line) > 0:
                logtsraw(line)

                cmd = get_action(line)
                if cmd is not None and ('do sample' == cmd['action']):
                    logger.debug('cmd: do sample')
                    borrow(1)

            if len(outqueue):
                xbeesend(outqueue.pop(0))

        except KeyboardInterrupt:
            raise
        
        except:
            logger.exception('')

        await asyncio.sleep(0.05)


async def taskBlink():
    while should_continue:
        usr3_on()
        green_on()
        await asyncio.sleep(0.05)
        usr3_off()
        green_off()
        await asyncio.sleep(1)


if '__main__' == __name__:

    logger.setLevel(logging.DEBUG)

    if not is_rpi():
        from node.drivers.indicators import *
        indicators_setup()

    tasks = [taskTrigger(), taskSampling(), ]
    if ser is not None:
        tasks.append(taskSerial())
    if not is_rpi():
        tasks.append(taskBlink())
    
    logger.info(__name__ + ' is ready')

    try:
        asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
    except KeyboardInterrupt:
        should_continue = False
        logger.info('user interrupted')

    if connection:
        connection.close()
    if ser:
        ser.close()
    if not is_rpi():
        indicators_cleanup()

    logger.info(__name__ + ' terminated')
