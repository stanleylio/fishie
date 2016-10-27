# Send a signed string to i7NUC via HTTP POST
# Messages are signed by the private key of this device
# Messages are verified by i7NUC with the public key of this device
#
# Targeted at the v4 API
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# University of Hawaii
# All Rights Reserved. 2016
import requests,json
from authstuff import get_signature
from helper import dt2ts
from os.path import expanduser,join
import socket


def prepare_message(m):
    """Sign, date, add own ID. Return as a dict()"""
    nodeid = socket.gethostname()
    #privatekey = open('/home/nuc/.ssh/id_rsa').read()
    privatekey = open(join(expanduser('~'),'.ssh/id_rsa')).read()
    sig = get_signature(m,privatekey)
    return {'src':nodeid,
            'ts':dt2ts(),
            'msg':m,
            'sig':sig,
            }

def post(m):
    endpoint = 'http://grogdata.soest.hawaii.edu/api/4'
    r = requests.post(endpoint,data=prepare_message(m))
    return r.text


if '__main__' == __name__:
    m = '"Oh no sweetie put your hand down We are looking for actual physicians."'
    print(post(m))
