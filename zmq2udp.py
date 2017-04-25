# Relay node messages to server. Basically a zmq-to-udp relay.
# Meant to be run on base stations.
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2016
import sys,json,traceback,socket
from os.path import expanduser
sys.path.append(expanduser('~'))
from node.zmqloop import zmqloop


nodeid = socket.gethostname()


# UDP link
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def send(d):
    s = json.dumps([nodeid,d],separators=(',',':'))
    sock.sendto(s,('128.171.153.115',9007))


def callback(m):
    try:
        print('= = = = = = = = = =')
        print(m.strip())
        send(m)
    except:
        traceback.print_exc()

zmqloop(callback)
