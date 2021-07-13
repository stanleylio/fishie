"""
"""
import pika, socket, sys, time, logging, argparse, json
from datetime import timedelta
from os.path import expanduser, basename, splitext
sys.path.append(expanduser('~'))
from node.parse_support import parse_message, pretty_print
from cred import cred


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


exchange = 'uhcm'
nodeid = socket.gethostname()
reconnection_delay = 3


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
    tags = ['*.samples', '*.s', '*.debug', '*.d', '*.rt']
    for tag in tags:
        channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=tag)
    channel.basic_consume(queue_name, callback, auto_ack=False)
    return connection, channel


def callback(ch, method, properties, body):
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

        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except UnicodeDecodeError:
        # ignore malformed messages
        logger.warning(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except:
        logger.exception(body)
        raise


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
            logger.exception('wut?')
            raise

        time.sleep(reconnection_delay)
