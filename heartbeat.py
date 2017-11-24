#!/usr/bin/python3
# Stanley H.I. Lio
# hlio@hawaii.edu
import sys,traceback,logging,pika,socket,time,shutil
from os.path import expanduser
sys.path.append(expanduser('~'))
from node.z import send
from cred import cred


logging.basicConfig(level=logging.DEBUG)
logging.getLogger('pika').setLevel(logging.WARNING)


exchange = 'uhcm'
nodeid = socket.gethostname()
routing_key = nodeid + '.debug'


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
        usage = shutil.disk_usage('/')
        d = {'system_clock':time.time(),'uptime_second':uptime_second,
             'usedMB':int(usage.used/1e6),'freeMB':int(usage.free/1e6)}
        try:
            from node.drivers.watchdog import Watchdog
            w = Watchdog(bus=1)
            d['VbattV'] = w.read_vbatt()
        except:
            traceback.print_exc()
        m = send(None,d).strip()
        logging.debug(m)
        
        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=m,
                              properties=pika.BasicProperties(delivery_mode=1,
                                                              content_type='text/plain',
                                                              expiration=str(5*60*1000)))
    except pika.exceptions.ConnectionClosed:
        connection,channel = None,None
        logging.error('connection closed')  # connection to the local exchange closed


connection,channel = None,None

logging.info(__name__ + ' is ready')
taskHeartbeat()
connection.close()
logging.info(__name__ + ' terminated')
