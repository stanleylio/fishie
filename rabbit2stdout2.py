import pika, sys, logging, socket
from os.path import basename,expanduser
sys.path.append(expanduser('~'))
from pika import exceptions
from pika.adapters import twisted_connection
from twisted.internet import defer, reactor, protocol, task
from twisted.internet.defer import setDebugging
from cred import cred


logging.basicConfig(level=logging.WARNING)
logging.getLogger('pika').setLevel(logging.WARNING)
setDebugging(True)


nodeid = socket.gethostname()
exchangename = 'uhcm'


@defer.inlineCallbacks
def run(connection):
    channel = yield connection.channel()
    #exchange = yield channel.exchange_declare(exchange=exchangename, type='topic', durable=True)
    result = yield channel.queue_declare(auto_delete=True, exclusive=True)
    yield channel.queue_bind(exchange=exchangename, queue=result.method.queue, routing_key='#')
    yield channel.basic_qos(prefetch_count=1)
    queue_object, consumer_tag = yield channel.basic_consume(queue=result.method.queue, no_ack=True)
    l = task.LoopingCall(read, queue_object)
    l.start(0.001)


@defer.inlineCallbacks
def read(queue_object):
    ch, method, properties, body = yield queue_object.get()
    if body:
        print('{}\t{}'.format(method.routing_key, body.strip()))
    #yield ch.basic_ack(delivery_tag=method.delivery_tag)


credentials = pika.PlainCredentials(nodeid, cred['rabbitmq'])
parameters = pika.ConnectionParameters(credentials=credentials)
cc = protocol.ClientCreator(reactor, twisted_connection.TwistedProtocolConnection, parameters)
d = cc.connectTCP('localhost', 5672)
d.addCallback(lambda protocol: protocol.ready)
d.addCallback(run)
reactor.run()
