# meant to be run on field stations
import sys,traceback,pika,socket
from os.path import expanduser
sys.path.append(expanduser('~'))
from node.zmqloop import zmqloop
from cred import cred


exchange = 'uhcm'
nodeid = socket.gethostname()


def rabbit_init():
    credentials = pika.PlainCredentials(nodeid,cred['rabbitmq'])
    connection = pika.BlockingConnection(pika.ConnectionParameters('128.171.153.115',5672,'/',credentials))
    channel = connection.channel()
    #channel.basic_qos(prefetch_count=10)
    channel.exchange_declare(exchange=exchange,type='topic',durable=True)
    return connection,channel

#channel.queue_delete(queue='base-004.rabbit2zmq')
#exit()

connection,channel = rabbit_init()

def callback(m):
    global connection
    global channel
    try:
        print('= = = = = = = = = =')
        print(m)
        channel.basic_publish(exchange=exchange,
                              routing_key=nodeid + '.samples',
                              body=m,
                              properties=pika.BasicProperties(delivery_mode=2,
                                                              content_type='text/plain',))
    except (pika.exceptions.ChannelClosed,pika.exceptions.ConnectionClosed):
        print('re-establishing rabbitmq connection...')
        connection,channel = rabbit_init()
    except:
        traceback.print_exc()

# application/json
# reply_to
# correlation_id

zmqloop(callback)
connection.close()
