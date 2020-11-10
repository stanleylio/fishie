# redirect RabbitMQ stuff to text file, with timestamps
#
# requiring queue (re)declare to match the existing queue is annoying.
# 
# Stanley H.I. Lio
# hlio@hawaii.edu
# University of Hawaii
# All Rights Reserved. 2018
import sys, pika, socket, logging, argparse
from os.path import exists, join, expanduser, basename
sys.path.append(expanduser('~'))
from datetime import datetime
from helper import dt2ts
from node.config.config_support import import_node_config
from cred import cred


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


exchange = 'uhcm'
nodeid = socket.gethostname()
reconnection_delay = 5

parser = argparse.ArgumentParser(description='log2txt.py')
parser.add_argument('--brokerip', metavar='broker', type=str, help='Broker IP', default='localhost')
parser.add_argument('--brokerport', metavar='port', type=int, help='Port', default=5672)
args = parser.parse_args()

def init_rabbit():
    credentials = pika.PlainCredentials(nodeid, cred['rabbitmq'])
    connection = pika.BlockingConnection(pika.ConnectionParameters(args.brokerip, args.brokerport, '/', credentials))
    channel = connection.channel()
    channel.basic_qos(prefetch_count=50)
    
    channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)
    result = channel.queue_declare(queue=basename(__file__),
                                   durable=True,
                                   arguments={'x-message-ttl':72*60*60*1000})

    queue_name = result.method.queue
    tags = ['*.samples', '*.s', '*.debug', '*.d']
    for tag in tags:
        channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=tag)
    channel.basic_consume(queue_name, callback, auto_ack=False)
    return connection, channel


if '__main__' == __name__:

    # product of this script: the raw text file
    config = import_node_config()
    output_path = getattr(config, 'log2txt_output_path', None)
    assert output_path is not None and exists(output_path)
    tsraw = open(join(output_path, 'tsraw.txt'), 'a', 1)

    def callback(ch, method, properties, body):
        print('= = = = =')
        print(body)

        dt = datetime.utcnow()
        tsraw.write('{}\t{:6f}\t{}\t{}\n'.format(dt.isoformat(), dt2ts(dt), method.routing_key, body.strip()))
        tsraw.flush()

        ch.basic_ack(delivery_tag=method.delivery_tag)

    connection, channel = init_rabbit()

    
    logger.info(__file__ + ' is ready')

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

        time.sleep(reconnection_delay)
        
    logger.info(__file__ + ' terminated')
    tsraw.close()
