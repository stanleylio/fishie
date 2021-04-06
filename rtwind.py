"""Poll the windbird signal conditioner, then compute summary statistics
and transmit the result to the local broker.

The raw readings are transmitted as .rt; the statistics as .s. Typically
the windbird is polled at a much higher rate than the statistics are
calculated (say 60:1 for 1second poll / 1minute summary).
 
Stanley H.I. Lio
"""
import sys, time, pika, socket, json, collections, logging, math, argparse, asyncio
from os.path import expanduser, exists
sys.path.append(expanduser('~'))
from scipy.stats import circmean
import numpy as np
from z import send
from drivers.rmy05106 import RMY05106
from helper import init_rabbit
from cred import cred


logger = logging.getLogger(__name__)


async def taskSummary():
    global should_continue, windhistory

    connection, channel = None, None
    last_transmitted = time.time()

    while should_continue:
        ts = time.time()

        # "sleep however many seconds til the end of this cycle"
        # "but if that turns out to be negative, then we are late and so we sleep 0 second"
        await asyncio.sleep(max(0, last_transmitted + AVG_WINDOW_SECOND - ts))

        try:
            if ts - last_transmitted >= AVG_WINDOW_SECOND:
                # remove stale entries (redundant if windbird responded to all requests)
                t,v,d = zip(*filter(lambda x: x[0] >= ts - AVG_WINDOW_SECOND, windhistory))

                logger.debug('len(windhistory)={}'.format(len(windhistory)))

                C = {}
                #C['ts'] = np.nanmean(t).item() if len(t) else float('nan')
                C['ts'] = ts    # !
                # average wind speed
                C['v'] = round(np.nanmean(v).item() if len(v) else float('nan'), 3)
                d = list(filter(lambda x: not math.isnan(x), d))
                # average direction
                # TODO: "... but only for those samples where wind_mps > some threshold"
                #http://www.ndbc.noaa.gov/wndav.shtml
                C['d'] = round(circmean(d, high=360, low=0).item() if len(d) else float('nan'), 1)
                # gust
                g = list(filter(lambda x: not math.isnan(x), v))
                C['g'] = round(max(g) if len(g) else float('nan'), 3)

                logger.info(C)
                
                if connection is None or channel is None:
                    connection, channel = init_rabbit(nodeid, cred['rabbitmq'])
                channel.basic_publish(exchange=exchange,
                                      routing_key=SENDER_ID + '.s',
                                      body=send(None, C, src=SENDER_ID).strip(),
                                      properties=pika.BasicProperties(delivery_mode=2,
                                                                      content_type='text/plain',
                                                                      expiration=str(10*24*3600*1000)))

                last_transmitted = ts
                
        except pika.exceptions.ConnectionClosed:
            connection, channel = None, None
            logger.error('connection closed')
        except:
            logger.exception('taskSummary')
            should_continue = False
            if connection:
                connection.close()
            raise


async def taskRTWind():
    global should_continue, windhistory

    connection, channel = None, None
    rmy = RMY05106(CONDITIONER_PORT, baud=BAUD)
    last_polled = time.time()

    while should_continue:
        ts = time.time()

        # Twisted actually schedules your thing at the frequency you
        # specify even if you overrun. But if you switch to asyncio then
        # you can't use sleep(PERIOD) to emulate that behavior since
        # serial port access takes significant amount of time.
        #await asyncio.sleep(POLL_PERIOD_SECOND)
        await asyncio.sleep(max(0, last_polled + POLL_PERIOD_SECOND - ts))
        
        try:
            r = rmy.read()
            d = None
            if r is not None:
                d = {'ts':time.time()}
                d.update(r)
                windhistory.append([d['ts'], d['v'], d['d']])
            else:
                logging.warning('No response from windbird')

            if d is not None:
                #print('\x1b[2J\x1b[;H')
                logger.info(d)

                if connection is None or channel is None:
                    connection, channel = init_rabbit(nodeid, cred['rabbitmq'])
                channel.basic_publish(exchange=exchange,
                                      routing_key=SENDER_ID + '.rt',
                                      body=send(None, d, src=SENDER_ID).strip(),
                                      properties=pika.BasicProperties(delivery_mode=1,
                                                                      content_type='text/plain',
                                                                      expiration=str(60*1000)))
        except pika.exceptions.ConnectionClosed:
            connection, channel = None, None
            logger.error('connection closed')
        except:
            logger.exception('taskRTWind')
            should_continue = False
            if connection:
                connection.close()
            raise


if __name__ == '__main__':
    
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('pika').setLevel(logging.WARNING)
    
    exchange = 'uhcm'
    nodeid = socket.gethostname()
    should_continue = True

    parser = argparse.ArgumentParser(description='ding')
    parser.add_argument('--AVG_WINDOW_SECOND', default=60, type=int, help='')
    parser.add_argument('--POLL_PERIOD_SECOND', default=1, type=float, help='')
    parser.add_argument('--CONDITIONER_PORT', default='/dev/ttyS0', type=str, help='')
    parser.add_argument('--BAUD', default=115200, type=int, help='')
    parser.add_argument('--SENDER_ID', default=nodeid, type=str, help='')
    args = parser.parse_args()
    AVG_WINDOW_SECOND = args.AVG_WINDOW_SECOND
    POLL_PERIOD_SECOND = args.POLL_PERIOD_SECOND
    CONDITIONER_PORT = args.CONDITIONER_PORT
    BAUD = args.BAUD
    SENDER_ID = args.SENDER_ID

    windhistory = collections.deque(maxlen=int(AVG_WINDOW_SECOND/POLL_PERIOD_SECOND))

    logging.debug('windhistory maxlen={}'.format(windhistory.maxlen))

    try:
        asyncio.get_event_loop().run_until_complete(asyncio.gather(
            taskRTWind(),
            taskSummary(),
            ))
    except KeyboardInterrupt:
        should_continue = False
        logging.info('user interrupted')

