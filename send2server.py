# Send a string to remote host via HTTP POST
#
# v4:
# Messages are signed by the private key of the sender device
# Messages are verified by remote host with the public key of the sender device
#
# v5:
# Messages are not signed. HTTP Basic Auth is used instead (need SSL...).
#
# Demo: If arguments are supplied, they are sent as individual messages to glazerlab-i7nuc.
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# University of Hawaii
# All Rights Reserved. 2017
from __future__ import division
import requests,time,socket
from authstuff import get_signature
from os.path import expanduser,join


node = socket.gethostname()


def prepare_message(m):
    """Sign, date, add own ID. Return as a dict()"""
    sig = get_signature(m,prepare_message.privatekey)
    return {'src':node,
            'ts':time.time(),
            'msg':m,
            'sig':sig,
            }
prepare_message.privatekey = open(join(expanduser('~'),'.ssh/id_rsa')).read().strip()

# custom public key authentication
def post4(m,endpoint):
    r = requests.post(endpoint,data=prepare_message(m))
    return r.text

# HTTP Basic Auth
def post5(m,endpoint,auth):
    r = requests.post(endpoint,
                      data={'m':m,'ts':time.time(),'src':node},
                      auth=auth)
    return r.text


if '__main__' == __name__:
    import sys
    sys.path.append(expanduser('~'))
    from cred import cred

    if len(sys.argv) > 1:
        for m in sys.argv[1:]:
            
            # API v4
            url = 'https://grogdata.soest.hawaii.edu/api/4'
            print(post4(m,url))

            # API v5
            url = 'https://grogdata.soest.hawaii.edu/api/5/raw'
            print(post5(m,url,('uhcm',cred['uhcm'])))
    
        exit()

    raw_input('No argument supplied. Proceed to benchmark?')
    
    # profiling v4
    # manage ~95 POST per minute from BBB to glazerlab-i7nuc
    # ~557 POST per minute from glazerlab-i7nuc to itself
    url = 'https://grogdata.soest.hawaii.edu/api/4'
    start_time = time.time()
    N = 100
    for i in range(N):
        m = '"single digit millionaires have no effective access to the legal system" "It is difficult to get a man to understand something, when his salary depends upon his not understanding it." "Surely, comrades, you don\'t want Jones back?" "Two possibilities exist: either we are alone in the universe, or we are not. Both are equally terrifying."'
        print(post4(m,url))
    stop_time = time.time()
    print('{} to {}, total {} seconds'.format(start_time,stop_time,stop_time-start_time))
    print('avg {:.1f} call/minute ({:.1f} call/second)'.format(N/(stop_time-start_time)*60,N/(stop_time-start_time)))

