#
# Stanley H.I. Lio
# hlio@hawaii.edu
# University of Hawaii
# All Rights Reserved, 2017
import pika,socket,traceback,sys,time,math,MySQLdb,logging,argparse
from os.path import expanduser,basename
sys.path.append(expanduser('~'))
from node.parse_support import parse_message,pretty_print
from node.storage.storage2 import storage
from cred import cred


logging.basicConfig(level=logging.WARNING)

parser = argparse.ArgumentParser(description="""Redirect RabbitMQ exchange UHCM to STDOUT. Example: python rabbit2stdout.py glazerlab-e5 base-004 node-027""")
parser.add_argument('sources',type=str,nargs='*')
args = parser.parse_args()


exchange = 'uhcm'
nodeid = socket.gethostname()
sources = args.sources

credentials = pika.PlainCredentials('nuc',cred['rabbitmq'])
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
channel = connection.channel()

channel.exchange_declare(exchange=exchange,type='topic',durable=True)
result = channel.queue_declare(queue=basename(__file__),
                               exclusive=True)

queue_name = result.method.queue


if len(sources) <= 0:
    logging.info('No source specified. Listening to *.samples')
    sources = ['*']
for source in sources:
    channel.queue_bind(exchange=exchange,
                       queue=queue_name,
                       routing_key=source + '.samples')

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
