#
# Stanley H.I. Lio
# hlio@hawaii.edu
# University of Hawaii
# All Rights Reserved, 2017
import pika,traceback,sys,logging,argparse,socket
from os.path import expanduser,basename
sys.path.append(expanduser('~'))
from cred import cred


logging.basicConfig(level=logging.INFO)


nodeid = socket.gethostname()


parser = argparse.ArgumentParser(description="""Redirect RabbitMQ exchange UHCM to STDOUT. Example: python rabbit2stdout.py glazerlab-e5.samples base-004.samples""")
parser.add_argument('sources',type=str,nargs='*')
args = parser.parse_args()

exchange = 'uhcm'
sources = args.sources

credentials = pika.PlainCredentials(nodeid,cred['rabbitmq'])
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
channel = connection.channel()
channel.exchange_declare(exchange=exchange,type='topic',durable=True)
result = channel.queue_declare(queue=basename(__file__),
                               exclusive=True)
queue_name = result.method.queue


if len(sources) <= 0:
    logging.info('No source specified. Listening to everything.')
    channel.queue_bind(exchange=exchange,
                       queue=queue_name,
                       routing_key='#')
else:
    for source in sources:
        channel.queue_bind(exchange=exchange,
                           queue=queue_name,
                           routing_key=source)
                           #routing_key=source + '.samples')

def callback(ch,method,properties,body):
    print(method.routing_key,body)
    #ch.basic_ack(delivery_tag=method.delivery_tag)


logging.info(__file__ + ' is ready')
channel.basic_consume(callback,queue=queue_name,no_ack=True)
try:
    channel.start_consuming()
except KeyboardInterrupt:
    logging.info('user interrupted')
logging.info(__file__ + ' terminated')
