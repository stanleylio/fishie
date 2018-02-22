#
# Stanley H.I. Lio
# hlio@hawaii.edu
# University of Hawaii
# All Rights Reserved, 2017
import pika, traceback, sys, logging, argparse, socket
from os.path import expanduser
sys.path.append(expanduser('~'))
from cred import cred


logging.basicConfig(level=logging.INFO)
logging.getLogger('pika').setLevel(logging.WARNING)


nodeid = socket.gethostname()


parser = argparse.ArgumentParser(description="""Show uhcm traffic. Example: python rabbit2stdout.py \"base-003.samples\" \"*.debug\"""")
parser.add_argument('topics', type=str, nargs='*')
args = parser.parse_args()

exchange = 'uhcm'
topics = args.topics

credentials = pika.PlainCredentials(nodeid, cred['rabbitmq'])
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
channel = connection.channel()
#channel.exchange_declare(exchange=exchange,type='topic', durable=True)
result = channel.queue_declare(exclusive=True, auto_delete=True)
queue_name = result.method.queue


if len(topics) <= 0:
    logging.info('No topic specified. Listening to everything.')
    topics = ['#']

for topic in topics:
    channel.queue_bind(exchange=exchange,
                       queue=queue_name,
                       routing_key=topic)

def callback(ch, method, properties, body):
    print('{}\t{}'.format(method.routing_key, body.strip()))
    #print(body.strip())
    #yield ch.basic_ack(delivery_tag=method.delivery_tag)


logging.debug(__file__ + ' is ready')
channel.basic_consume(callback, queue=queue_name, exclusive=True, no_ack=True)
try:
    channel.start_consuming()
except KeyboardInterrupt:
    logging.debug('user interrupted')
connection.close()
logging.debug(__file__ + ' terminated')
