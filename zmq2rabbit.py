# meant to be run on field stations
import sys,traceback,pika,socket,logging,time
from os.path import expanduser
sys.path.append(expanduser('~'))
from node.zmqloop import zmqloop
from cred import cred


exchange = 'uhcm'
nodeid = socket.gethostname()

logging.basicConfig(level=logging.INFO)


def rabbit_init():
    credentials = pika.PlainCredentials(nodeid,cred['rabbitmq'])
    #connection = pika.BlockingConnection(pika.ConnectionParameters('128.171.153.115',5672,'/',credentials))
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
    channel = connection.channel()
    #channel.basic_qos(prefetch_count=10)
    channel.exchange_declare(exchange=exchange,type='topic',durable=True)
    return connection,channel

#channel.queue_delete(queue='base-004.rabbit2zmq')
#exit()


#connection,channel = None,None
connection,channel = rabbit_init()
def callback(m):
    global connection   # pass as *args?
    global channel

    try:
        if connection is None or channel is None:
            connection,channel = rabbit_init()
            logging.info('connection re-established')
        
        print('= = = = = = = = = =')
        print(m)
        channel.basic_publish(exchange=exchange,
                              routing_key=nodeid + '.samples',
                              body=m,
                              properties=pika.BasicProperties(delivery_mode=2,
                                                              content_type='text/plain',
                                                              expiration=str(24*3600),
                                                              timestamp=time.time()))
    except pika.exceptions.ConnectionClosed:
        connection,channel = None,None
        logging.error('connection closed')
        time.sleep(5)
    except:
        traceback.print_exc()


zmqloop(callback)
connection.close()
