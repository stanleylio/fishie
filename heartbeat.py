import sys,traceback,logging,pika,socket,time
from os.path import expanduser
sys.path.append(expanduser('~'))
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from node.z import send
from cred import cred


logging.basicConfig(level=logging.DEBUG)
logging.getLogger('pika').setLevel(logging.WARNING)


exchange = 'uhcm'
nodeid = socket.gethostname()
routing_key = nodeid + '.monitor'


def rabbit_init():
    credentials = pika.PlainCredentials(nodeid,cred['rabbitmq'])
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange,exchange_type='topic',durable=True)
    return connection,channel


def taskHeartbeat():
    try:
        global channel,connection
        if connection is None or channel is None:
            connection,channel = rabbit_init()

        uptime_second = float(open('/proc/uptime').readline().split()[0])

        d = {'system_clock':time.time(),'uptime_second':uptime_second}
        m = send(None,d).strip()
        logging.debug(m)
        
        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=m,
                              properties=pika.BasicProperties(delivery_mode=1,
                                                              content_type='text/plain',
                                                              expiration=str(5*60*1000),
                                                              timestamp=time.time()))
    except pika.exceptions.ConnectionClosed:
        connection,channel = None,None
        logging.error('connection closed')  # connection to the local exchange closed


connection,channel = None,None

logging.info(__name__ + ' is ready')
LoopingCall(taskHeartbeat).start(60)
reactor.run()
connection.close()
logging.info(__name__ + ' terminated')
