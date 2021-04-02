"""
Cache stuff received from the RabbitMQ exchange in Redis. This keeps the
latest readings from the instruments in redis to speed up dashboard
creation.

RabbitMQ is a godsend.

Stanley H.I. Lio
hlio@hawaii.edu
University of Hawaii, 2021
"""
import pika, socket, sys, time, math, logging, argparse, redis, json, random
from datetime import timedelta
from os.path import expanduser, basename, splitext
sys.path.append(expanduser('~'))
from node.parse_support import parse_message, pretty_print
from cred import cred


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# - - - - -
reconnection_delay_second = 11
redis_TTL_second = int(timedelta(days=1).total_seconds())
exchange = 'uhcm'
# - - - - -

nodeid = socket.gethostname()


parser = argparse.ArgumentParser(description='wut')
parser.add_argument('--brokerip', metavar='broker', type=str, help='Broker IP', default='localhost')
parser.add_argument('--brokerport', metavar='port', type=int, help='Port', default=5672)
args = parser.parse_args()


redis_server = redis.StrictRedis(host='localhost', port=6379, db=0)
#redis_server.flushall()


def init_rabbit():
    credentials = pika.PlainCredentials(nodeid, cred['rabbitmq'])
    connection = pika.BlockingConnection(pika.ConnectionParameters(args.brokerip, args.brokerport, '/', credentials))
    channel = connection.channel()
    channel.basic_qos(prefetch_count=16)

    channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)
    queue_name = "{}_{}".format(nodeid, splitext(basename(__file__))[0])
    result = channel.queue_declare(queue=queue_name,
                                   durable=True,
                                   arguments={'x-message-ttl':2**31-1}) # ~24 days.

    #queue_name = result.method.queue
    tags = ['*.samples', '*.s', '*.debug', '*.d']
    for tag in tags:
        channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=tag)
    channel.basic_consume(queue_name, callback, auto_ack=False)
    return connection, channel


def callback(ch, method, properties, body):
    global redis_server
    try:
        rt = time.time()
        body = body.decode()
        d = parse_message(body)
        if d is None:
            logger.warning('Unrecognized: ' + body)
        else:
            d['ReceptionTime'] = rt
            print('= = = = = = = = = = = = = = =')
            pretty_print(d)

            for k in d.keys():
                try:
                    if math.isnan(d[k]):
                        d[k] = None
                except TypeError:
                    pass

            for k,v in d.items():
                #print(k,v)
                # frigging json everywhere... "impedance mismatch"...
                redis_server.set('latest:{}:{}'.format(d['node'], k),
                                 json.dumps((d['ReceptionTime'], v)),
                                 ex=int(redis_TTL_second),
                                 )

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except UnicodeDecodeError:
        # ignore malformed messages
        logger.warning(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except KeyboardInterrupt:
        raise
    except:
        logger.exception(body)


if '__main__' == __name__:

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('pika').setLevel(logging.WARNING)

    connection, channel = init_rabbit()
    
    while True:
        try:
            if connection is None or channel is None:
                connection, channel = init_rabbit()
            channel.start_consuming()
            
        except KeyboardInterrupt:
            logger.info('user interrupted')
            break
        
        except (pika.exceptions.ConnectionClosedByBroker, pika.exceptions.AMQPConnectionError):
            logger.exception('broker stuff')
            connection, channel = None, None
            
        except:
            logging.exception('wut?')

        time.sleep(reconnection_delay_second)


if connection:
    connection.close()
