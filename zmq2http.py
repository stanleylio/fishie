# relay xbee msgs (from zmq 9002) to HTTP POST v4 API
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2017
import sys,json,traceback,socket
from os.path import expanduser
sys.path.append(expanduser('~'))
from node.send2server import post4
from zmqloop import zmqloop


nodeid = socket.gethostname()


def send(d):
    m = json.dumps([nodeid,d],separators=(',',':'))
    logger.debug(post4(m,'https://grogdata.soest.hawaii.edu/api/4'))


def callback(m):
    print('= = = = = = = = = =')
    print(m)
    try:
        send(m)
    except:
        traceback.print_exc()

zmqloop(callback)
