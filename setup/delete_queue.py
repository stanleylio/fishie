import sys,pika,argparse
from os.path import expanduser
sys.path.append(expanduser('~'))
from cred import cred


parser = argparse.ArgumentParser(description='')
parser.add_argument('queue_name',metavar='daq',type=str,
                    help='name of queue to be deleted')
args = parser.parse_args()
print(args.queue_name)

credentials = pika.PlainCredentials('nuc',cred['rabbitmq'])
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
channel = connection.channel()
channel.queue_delete(queue=args.queue_name)
connection.close()
