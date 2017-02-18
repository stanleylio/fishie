# Send a string to i7NUC via HTTP POST
# Messages are signed by the private key of this device
# Messages are verified by i7NUC with the public key of this device
#
# Targeted at the v4 API
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# University of Hawaii
# All Rights Reserved. 2016
import requests,time
from authstuff import get_signature
from os.path import expanduser,join
import socket


def prepare_message(m):
    """Sign, date, add own ID. Return as a dict()"""
    #privatekey = open('/home/nuc/.ssh/id_rsa').read()
    privatekey = open(join(expanduser('~'),'.ssh/id_rsa')).read()
    sig = get_signature(m,privatekey)
    return {'src':socket.gethostname(),
            'ts':time.time(),
            'msg':m,
            'sig':sig,
            }

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
        m = '"Surely, comrades, you don\'t want Jones back?"'
        print(post(m,url))
