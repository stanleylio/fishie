# 0MQ -> STDOUT, one line per message
# Example: python zmqprint.py 127.0.0.1:9002 --topic kmet1
# --topic is optional.
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2017
import zmq,sys,json,logging,traceback,argparse
from os.path import expanduser
sys.path.append(expanduser('~'))
from node.zmqloop import zmqloop


parser = argparse.ArgumentParser(description="""Redirect zmq to STDOUT. Example: python zmq2stdout.py 127.0.0.1:9002 --topic kmet1""")
parser.add_argument('zmq_sockets',type=str,nargs='+')
parser.add_argument('--topic',dest='zmq_topic',default=u'',type=unicode)
args = parser.parse_args()


def callback(m):
    try:
        sys.stdout.write(m + '\n')  # ?
        sys.stdout.flush()
    except:
        traceback.print_exc()


zmqloop(callback,topic=args.zmq_topic)
