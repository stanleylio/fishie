# Real-time wind and (avg + gust) server
# 
#
# TODO: let avr calculate running average
#
# It's complicated to support different sampling rates for different variables
# Each var would have to have a defined interval, and script would need to know
# to group variables with same sampling interval together, along with timestamp
# (while not considering timsetamp's own interval)...
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# 2018
import time, pika, socket, json, collections, statistics, logging, math, argparse
from twisted.web import xmlrpc, server
from twisted.internet.task import LoopingCall
from twisted.logger import Logger
from scipy.stats import circmean
import numpy as np
from z import send
from parse_support import pretty_print
from drivers.rmy05106 import RMY05106
from cred import cred


logging.getLogger('pika').setLevel(logging.WARNING)


parser = argparse.ArgumentParser(description='ding')
parser.add_argument('--WIND_AVG_WINDOW_SECOND', default=60, type=int, help='')
parser.add_argument('--WIND_PERIOD_SECOND', default=1, type=float, help='')
parser.add_argument('--WIND_PORT', default='/dev/ttyS0', type=str, help='')
parser.add_argument('--WIND_BAUD', default=115200, type=int, help='')

args = parser.parse_args()

WIND_AVG_WINDOW_SECOND = args.WIND_AVG_WINDOW_SECOND
WIND_PERIOD_SECOND = args.WIND_PERIOD_SECOND
WIND_PORT = args.WIND_PORT
WIND_BAUD = args.WIND_BAUD

exchange = 'uhcm'
nodeid = socket.gethostname()
sender_id = nodeid

log = Logger()


def rabbit_init():
    credentials = pika.PlainCredentials(nodeid, cred['rabbitmq'])
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)
    return connection, channel


connection, channel = None, None
tags = ['ts', 'v', 'd']
windhistory = collections.deque(maxlen=int(WIND_AVG_WINDOW_SECOND/WIND_PERIOD_SECOND))


class WindServer(xmlrpc.XMLRPC):
    '''Return wind speed and direction averages, as well as gust'''
    def xmlrpc_read(self):
        C = {}
        try:
            # remove stale entries (redundant if windbird responded to all requests)
            tmp = filter(lambda x: x[0] >= time.time() - WIND_AVG_WINDOW_SECOND, windhistory)
            r = list(zip(*tmp))
            
            C['ts'] = np.nanmean(r[0]).item() if len(r[0]) else float('nan')
            C['v'] = np.nanmean(r[1]).item() if len(r[1]) else float('nan')
# TODO: "... but only for those samples where wind_mps > some threshold"
#http://www.ndbc.noaa.gov/wndav.shtml
            tmp = list(filter(lambda x: not math.isnan(x), r[2]))
            C['d'] = circmean(tmp, high=360, low=0).item() if len(tmp) else float('nan')
            tmp = list(filter(lambda x: not math.isnan(x), r[1]))
            C['g'] = max(tmp) if len(tmp) else float('nan')
        except:
            logging.exception('something wrong with windhistory')
            logging.error(str(windhistory))
        return C


def taskRTWind():
    global connection, channel
    
    #if connection is None or channel is None:
    #    connection,channel = rabbit_init()

    try:
        rmy = RMY05106(WIND_PORT, baud=WIND_BAUD)
        r = rmy.read()
        d = None
        if r is not None:
            d = {'ts':time.time()}
            d.update(r)
            windhistory.append([d[tag] for tag in tags])
        else:
            #windhistory.append([float('nan') for _ in tags])
            logging.warning('No response from windbird')

        if d is not None:
            #print('\x1b[2J\x1b[;H')
            pretty_print(d)
            m = send(None, d, src=sender_id).strip()

            if connection is None or channel is None:
                connection, channel = rabbit_init()
            channel.basic_publish(exchange=exchange,
                                  routing_key=sender_id + '.rt',
                                  body=m,
                                  properties=pika.BasicProperties(delivery_mode=1,
                                                                  content_type='text/plain',
                                                                  expiration=str(60*1000)))
                                                                  #timestamp=int(time.time())
    except pika.exceptions.ConnectionClosed:
        connection, channel = None, None
        logging.error('connection closed')  # connection to the local exchange closed? wut?
    except:
        logging.exception('taskRTWind')
										  


if __name__ == '__main__':
    
    from twisted.internet import reactor

    logging.basicConfig(level=logging.DEBUG)
    
    r = WindServer()
    reactor.listenTCP(7080, server.Site(r))
    LoopingCall(taskRTWind).start(WIND_PERIOD_SECOND)
    reactor.run()

    if connection:
        connection.close()

