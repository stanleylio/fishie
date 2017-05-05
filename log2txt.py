# redirect RabbitMQ stuff to text file, with timestamps
#
# requiring queue (re)declare to match the existing queue is annoying.
# 
# Stanley H.I. Lio
# hlio@hawaii.edu
# University of Hawaii
# All Rights Reserved, 2017
import sys,pika,socket,logging
from os.path import exists,join,expanduser,basename
sys.path.append(expanduser('~'))
from datetime import datetime
from helper import dt2ts
from node.config.config_support import import_node_config
from cred import cred


exchange = 'uhcm'
nodeid = socket.gethostname()


logging.basicConfig(level=logging.INFO)


credentials = pika.PlainCredentials('nuc',cred['rabbitmq'])
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
channel = connection.channel()
channel.exchange_declare(exchange=exchange,type='topic',durable=True)
result = channel.queue_declare(queue=basename(__file__),
                               durable=True,
                               arguments={'x-message-ttl':72*60*60*1000})

queue_name = result.method.queue
channel.queue_bind(exchange=exchange,
                   queue=queue_name,
                   routing_key='*.samples')


# product of this script: the raw text file
config = import_node_config()
output_path = getattr(config,'log2txt_output_path',None)
assert output_path is not None and exists(output_path)

raw = open(join(output_path,'raw.txt'),'a',0)
tsraw = open(join(output_path,'tsraw.txt'),'a',0)

def callback(ch,method,properties,body):
    print('= = = = = = = = = =')
    print(body)

    raw.write(body.strip() + '\n')
    dt = datetime.utcnow()
    tsraw.write('{}\t{:6f}\t{}\n'.format(dt.isoformat(),dt2ts(dt),body.strip()))

    raw.flush()
    tsraw.flush()

    ch.basic_ack(delivery_tag=method.delivery_tag)

logging.info(__file__ + ' is ready')
channel.basic_consume(callback,queue=queue_name)    # ,no_ack=True
try:
    channel.start_consuming()
except KeyboardInterrupt:
    logging.info('user interrupted')
logging.info(__file__ + ' terminated')

raw.close()
tsraw.close()
