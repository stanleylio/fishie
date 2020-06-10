# Fetch sensor data from broker to database.
#
# So publish/subscribe doesn't revolve around queues (except when used as a work queue).
# Fanout is done on the exchange level, so each consumer should have its own queue to
# receive a copy of the same message.
#
# Persistence: if the queue is not durable, there's no point in switching over to RabbitMQ
# from 0mq; if the queue is durable, then it's one more name to remember (monitor). And if
# TTL is not set, undelivered messages could fill up disk space if consumer is down.
#
# TTL: Per-queue or per-message?
# Policies for the X2mysql, X2stdout, X2txt etc. are different (X2mysql wants everything,
# X2stdout wants only the fresh ones).
#
# TTL=72hr means I have 72hr to detect and mitigate a problem before data loss.
# Though are they discarded or are they dead-lettered? TODO
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# University of Hawaii, 2020
import pika, socket, sys, time, math, MySQLdb, logging, argparse, redis, json, random
from datetime import timedelta
from os.path import expanduser, basename
sys.path.append(expanduser('~'))
from node.parse_support import parse_message, pretty_print
from node.storage.storage2 import Storage
from cred import cred


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


exchange = 'uhcm'
nodeid = socket.gethostname()
reconnection_delay = 5

parser = argparse.ArgumentParser(description='wut')
parser.add_argument('--brokerip', metavar='broker', type=str, help='Broker IP', default='localhost')
parser.add_argument('--brokerport', metavar='port', type=int, help='Port', default=5672)
args = parser.parse_args()


def init_rabbit():
    credentials = pika.PlainCredentials(nodeid, cred['rabbitmq'])
    connection = pika.BlockingConnection(pika.ConnectionParameters(args.brokerip, args.brokerport, '/', credentials))
    channel = connection.channel()
    channel.basic_qos(prefetch_count=32)

    channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)
    result = channel.queue_declare(queue=basename(__file__),
                                   durable=True,
                                   arguments={'x-message-ttl':2**31-1}) # ~24 days.

    queue_name = result.method.queue
    tags = ['*.samples', '*.s', '*.debug', '*.d']
    for tag in tags:
        channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=tag)
    channel.basic_consume(queue_name, callback, auto_ack=False)
    return connection, channel

store = Storage()
redis_server = redis.StrictRedis(host='localhost', port=6379, db=0)
#redis_server.flushall()

def callback(ch, method, properties, body):
    global store, redis_server
    try:
        body = body.decode()
        d = parse_message(body)
        if d is None:
            logger.warning('Unrecognized: ' + body)
        else:
            d['ReceptionTime'] = time.time()
            print('= = = = = = = = = = = = = = =')
            pretty_print(d)

            for k in d.keys():
                try:
                    if math.isnan(d[k]):
                        d[k] = None
                except TypeError:
                    pass

            store.insert(d['node'], d, reload_schema=random.random() > 0.95)

        ch.basic_ack(delivery_tag=method.delivery_tag)

        # optional cache (after acknowledgement - presumably broker can drop the message and it's in the db now)
        for k,v in d.items():
            #print(k,v)
            # frigging json everywhere... "impedance mismatch"...
            redis_server.set('latest:{}:{}'.format(d['node'], k), json.dumps((d['ReceptionTime'], v)), ex=int(timedelta(days=1).total_seconds()))
        
    except UnicodeDecodeError:
        # ignore malformed messages
        logger.warning(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except (MySQLdb.ProgrammingError, MySQLdb.OperationalError):
        logger.exception('db error')
        store = Storage()
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

        time.sleep(reconnection_delay)
