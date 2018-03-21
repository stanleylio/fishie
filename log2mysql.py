# This taps into the local RabbitMQ exchange and store .samples msgs into MySQL
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
# uhcm.poh.*.samples?
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# University of Hawaii
# All Rights Reserved, 2017
import pika, socket, traceback, sys, time, math, MySQLdb, logging, argparse
from os.path import expanduser,basename
sys.path.append(expanduser('~'))
from node.parse_support import parse_message, pretty_print
from node.storage.storage2 import storage
from cred import cred


logging.basicConfig(level=logging.DEBUG)
logging.getLogger('pika').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


exchange = 'uhcm'
nodeid = socket.gethostname()
reconnection_delay = 5

parser = argparse.ArgumentParser(description='log2txt.py')
parser.add_argument('--brokerip', metavar='broker', type=str,
                    help='Broker IP', default='localhost')
parser.add_argument('--brokerport', metavar='port', type=int,
                    help='Port', default=5672)
args = parser.parse_args()


def mq_init():
    credentials = pika.PlainCredentials(nodeid, cred['rabbitmq'])
    connection = pika.BlockingConnection(pika.ConnectionParameters(args.brokerip, args.brokerport, '/', credentials))
    channel = connection.channel()
    channel.basic_qos(prefetch_count=200)

    channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)
    result = channel.queue_declare(queue=basename(__file__),
                                   durable=True,
                                   arguments={'x-message-ttl':2**31-1}) # ~24 days.
    # this 32-bit limit is imposed by pika I guess. RMQ's limit is large enough to "not matter", according to the official response.

    queue_name = result.method.queue
    #for source in sources:
    #    channel.queue_bind(exchange=exchange,
    #                       queue=queue_name,
    #                       routing_key=source + '.samples') # or just '*.samples'
    channel.queue_bind(exchange=exchange,
                       queue=queue_name,
                       routing_key='*.samples')
    channel.queue_bind(exchange=exchange,
                       queue=queue_name,
                       routing_key='*.debug')
    channel.basic_consume(callback, queue=queue_name)    # ,no_ack=True
    return connection, channel

def init_storage():
    return storage()
store = init_storage()


def callback(ch, method, properties, body):
    global store
    #print(method.routing_key, body)
    try:
        body = body.decode()
        d = parse_message(body)
        if d is None:
            print('Message from unrecognized source: ' + body)
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

            store.insert(d['node'], d)

        # tigher than leaving this at the end.
        # some messages are not meant to be parsed though, like "node-NNN online" etc.
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except UnicodeDecodeError:
        logger.exception(body)
        # ignore malformed messages
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except (MySQLdb.ProgrammingError, MySQLdb.OperationalError):
        traceback.print_exc()
        store = init_storage()
    except KeyboardInterrupt:
        raise
    except:
        #traceback.print_exc()
        logger.exception(body)

    #ch.basic_ack(delivery_tag=method.delivery_tag)


logger.info(__file__ + ' is ready')
while True:
    try:
        connection, channel = mq_init()
        channel.start_consuming()
    except KeyboardInterrupt:
        logger.info('user interrupted')
        break
    except:
        logger.error('connection to broker closed')
        connection, channel = None, None
        time.sleep(reconnection_delay)
logger.info(__file__ + ' terminated')
