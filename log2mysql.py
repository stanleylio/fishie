"""Move sensor data from broker to database.

So publish/subscribe doesn't revolve around queues (except when used as
a work queue). Fanout is done on the exchange level, so each consumer
should have its own queue to receive a copy of the same message.

On persistence: RabbitMQ is nice because it lets you mess with your
consumer code while it holds the incoming messages for you. If you let
the server choose a random queue name for you, then you can't make it
durable since otherwise you won't be able to find that queue again on
restart. On the other hand, if you explicitly name the queue and make it
durable, then you need to remember to manually delete the queue when you
change the naming scheme, since the old queue would stick around
accumulating messages and quickly consuming your disk space.

TTL: Per-queue or per-message? Policies for the X2mysql, X2stdout, X2txt
etc. are different (X2mysql wants everything, X2stdout wants only the
fresh ones). TTL=72hr means I have 72hr to detect and mitigate a problem
before data loss.

Stanley H.I. Lio
"""
import pika, socket, sys, time, math, MySQLdb, logging, argparse, json, random
from datetime import timedelta
from os.path import expanduser, basename, splitext
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


store = Storage()


def callback(ch, method, properties, body):
    global store
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

            store.insert(d['node'], d, reload_schema=random.random() > 0.95)

        ch.basic_ack(delivery_tag=method.delivery_tag)
        
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
