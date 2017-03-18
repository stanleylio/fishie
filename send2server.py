# Send a string to remote host via HTTP POST
# Messages are signed by the private key of the sender device
# Messages are verified by remote host with the public key of the sender device
#
# Demo: If arguments are supplied, they are sent as individual messages to glazerlab-i7nuc.
#
# Targeted at the v4 API
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# University of Hawaii
# All Rights Reserved. 2016
import requests,time,socket
from authstuff import get_signature
from os.path import expanduser,join


def prepare_message(m):
    """Sign, date, add own ID. Return as a dict()"""
    sig = get_signature(m,prepare_message.privatekey)
    return {'src':socket.gethostname(),
            'ts':time.time(),
            'msg':m,
            'sig':sig,
            }
prepare_message.privatekey = open(join(expanduser('~'),'.ssh/id_rsa')).read().strip()


def post(m,endpoint):
    r = requests.post(endpoint,data=prepare_message(m))
    return r.text


if '__main__' == __name__:
    import sys

    url = 'http://grogdata.soest.hawaii.edu/api/4'
    
    if len(sys.argv) > 1:
        for m in sys.argv[1:]:
            print(post(m,url))
    else:
        print(time.time())
        for i in range(1):
            m = '"single digit millionaires have no effective access to the legal system" "It is difficult to get a man to understand something, when his salary depends upon his not understanding it." "Surely, comrades, you don\'t want Jones back?" "Two possibilities exist: either we are alone in the universe, or we are not. Both are equally terrifying."'
            post(m,url)
        print(time.time())
