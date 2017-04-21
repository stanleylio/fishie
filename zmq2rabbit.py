# meant to be run on field stations
import pika,socket


exchange = 'uhcm'
nodeid = socket.gethostname()


credentials = pika.PlainCredentials(nodeid,'playitsam')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.15',5672,'/',credentials))
channel = connection.channel()
#channel.basic_qos(prefetch_count=10)
channel.exchange_declare(exchange=exchange,type='topic',durable=True)

#channel.queue_delete(queue='base-004.rabbit2zmq')
#exit()

for i in range(1000):
    channel.basic_publish(exchange=exchange,
                          routing_key=nodeid + '.samples',
                          body='beatings will continue until morale improves {}'.format(i),
                          properties=pika.BasicProperties(delivery_mode=2,
                                                          content_type='text/plain',))
    # application/json
    # reply_to
    # correlation_id

connection.close()

