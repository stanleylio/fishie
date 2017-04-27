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
from twisted.internet import reactor
from node.wsrelay import BroadcastServerProtocol,BroadcastServerFactory
from autobahn.twisted.websocket import WebSocketServerFactory,\
     WebSocketServerProtocol,\
     listenWS


print('Not that easy. both rabbitmq blockingconnection and autobahn want to run their own loop.')
exit()

logging.basicConfig(level=logging.WARNING)

parser = argparse.ArgumentParser(description="""Redirect RabbitMQ exchange UHCM to WebSocket. Example: python rabbit2ws.py 9000""")
parser.add_argument('ws_port',type=int)
args = parser.parse_args()

ServerFactory = BroadcastServerFactory
factory = ServerFactory(u'ws://*:{}'.format(args.ws_port))
factory.protocol = BroadcastServerProtocol
listenWS(factory)

exchange = 'uhcm'
nodeid = socket.gethostname()

def on_channel_closed(channel,reply_code,reply_text):
    connection.close()

def on_channel_open(channel):
    channel.add_on_close_callback(on_channel_closed)

def on_connection_open(connection):
    connection.channel(on_open_callback=on_channel_open)

def on_connection_closed(connection,reply_code,reply_text):
    connection.ioloop.stop()

credentials = pika.PlainCredentials(nodeid,cred['rabbitmq'])
connection = pika.SelectConnection(pika.ConnectionParameters('localhost',5672,'/',credentials),
                                   on_connection_open,
                                   stop_ioloop_on_close=False)
connection.add_on_close_callback(on_connection_closed)

channel.exchange_declare(exchange=exchange,type='topic',durable=True)
result = channel.queue_declare(queue=basename(__file__),
                               exclusive=True)

queue_name = result.method.queue

channel.queue_bind(exchange=exchange,
                   queue=queue_name,
                   routing_key='*.samples')     # TODO

def callback(ch,method,properties,body):
    #print(method.routing_key,body)
    print(body)
    factory.broadcast(body)
    #ch.basic_ack(delivery_tag=method.delivery_tag)


logging.info(__file__ + ' is ready')
channel.basic_consume(callback,queue=queue_name,no_ack=True)



reactor.run()

try:
    channel.start_consuming()
except KeyboardInterrupt:
    logging.info('user interrupted')
logging.info(__file__ + ' terminated')
