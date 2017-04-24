# This one uses RabbitMQ.
# Meant to be run on the server (where the db and the exchange is)
#
# So publish/subscribe doesn't revolve around queues (except when used as a work queue).
# Fanout is done on the exchange level, so each consumer should have its own queue to
# receive a copy of the same message.
#
# Persistence: if the queue is not durable, there's no point in switching over to RabbitMQ
# from 0mq; if the queue is durable and TTL is unlimited, undelivered messages would take up
# space when consumer is down.
#
# TTL: Doing it per-queue. There's the per-message option too, but policies for
# the X2mysql, X2stdout, X2txt etc. are different (X2mysql wants everything, X2stdout
# wants only the fresh ones).
#
# TTL=24hr means I have 24hr to detect and mitigate a problem before data loss.
# Though are they discarded or are they dead-lettered?
#
# It lets you choose queue-level TTL and message level TTL. Amazing.
#
# uhcm.poh.*.samples?
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# University of Hawaii
# All Rights Reserved, 2017
import pika,socket,traceback,sys,time,math,MySQLdb,logging
from os.path import expanduser,basename
sys.path.append(expanduser('~'))
from node.parse_support import parse_message,pretty_print
from node.storage.storage2 import storage
from cred import cred


logging.basicConfig(level=logging.WARNING)


exchange = 'uhcm'
nodeid = socket.gethostname()
sources = ['base-001','base-003','base-004','glazerlab-e5','node-017','base-005']

credentials = pika.PlainCredentials(nodeid,cred['rabbitmq'])
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
channel = connection.channel()
#channel.queue_delete(queue='glazerlab-e5.rabbit2zmq')
#exit()

channel.exchange_declare(exchange=exchange,type='topic',durable=True)
result = channel.queue_declare(queue=nodeid + '.' + basename(__file__),
                               durable=True,
                               arguments={'x-message-ttl':24*60*60*1000})

queue_name = result.method.queue
for source in sources:
    channel.queue_bind(exchange=exchange,
                       queue=queue_name,
                       routing_key=source + '.samples')

def init_storage():
    return storage()
store = init_storage()

def callback(ch,method,properties,body):
    global store
    #print(method.routing_key,body)
    try:
        d = parse_message(body)
        if d is None:
            print('Message from unrecognized source: ' + body)
        else:
            d['ReceptionTime'] = time.time()
            print('= = = = = = = = = = = = = = =')
            pretty_print(d)

            # * * * HACK * * *
            if d['node'] == 'node-007' and 'ts' in d:
                d['Timestamp'] = d['ts']
            # * * * /HACK * * *

            for k in d.keys():
                try:
                    if math.isnan(d[k]):
                        d[k] = None
                except TypeError:
                    pass

            table = d['node']
            tmp = {k:d[k] for k in store.get_list_of_columns(table) if k in d}
            store.insert(table,tmp)
    except MySQLdb.OperationalError,e:
        #if e.args[0] in (MySQLdb.constants.CR.SERVER_GONE_ERROR,MySQLdb.constants.CR.SERVER_LOST):
        # e.g. a mysql server restart
        store = init_storage()
        traceback.print_exc()
        print(e)
    except:
        traceback.print_exc()
        print(body)

    ch.basic_ack(delivery_tag=method.delivery_tag)


logging.info(__file__ + ' is ready')
channel.basic_consume(callback,queue=queue_name)    # ,no_ack=True
try:
    channel.start_consuming()
except KeyboardInterrupt:
    logging.info('user interrupted')
logging.info(__file__ + ' terminated')
