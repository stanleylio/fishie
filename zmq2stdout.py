# 0MQ -> STDOUT, one line per message
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2017
import sys,traceback,argparse
from os.path import expanduser
sys.path.append(expanduser('~'))
from node.zmqloop import zmqloop


parser = argparse.ArgumentParser(description="""Redirect zmq to STDOUT.
Example: python zmq2stdout.py --topic kmet1 --port 127.0.0.1:9002""")
parser.add_argument('--topic',dest='zmq_topic',default=u'',type=unicode,
                    metavar='TOPIC',help='zmq topic to subscribe to. Default = "" (everything)')
parser.add_argument('--port',dest='zmq_port',default=['127.0.0.1:9002'],type=str,nargs='+',
                    metavar='PORT',help='zmq port to subscribe to. Default = 127.0.0.1:9002')
args = parser.parse_args()

def callback(m):
    try:
        sys.stdout.write(m.strip() + '\n') # ?
        sys.stdout.flush()
    except:
        traceback.print_exc()

zmqloop(callback,topic=args.zmq_topic,feeds=args.zmq_port)
sys.stdout.flush()
