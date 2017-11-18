#!/usr/bin/python3
# v5:
# Messages are not signed. HTTP Basic Auth is used instead (rely on SSL).
#
# [deprecated] v4:
# Messages are signed by the private key of the sender device
# Messages are verified by remote host with the public key of the sender device
#
# Demo: If arguments are supplied, they are sent as individual messages to glazerlab-i7nuc.
# If not, a list of sender's IPs is sent.
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# University of Hawaii
# All Rights Reserved. 2017
from __future__ import division
import requests,time,socket,json,subprocess
#from authstuff import get_signature
from os.path import expanduser,join,exists


nodeid = socket.gethostname()


def getIP():
    proc = subprocess.Popen(['hostname -I'],stdout=subprocess.PIPE,shell=True)
    out,err = proc.communicate()
    ips = out.decode().strip().split(' ')
    return ips


url = 'https://grogdata.soest.hawaii.edu/api/5/raw'
def post5(m,endpoint,auth):
    """POST a string to an endpoint"""
    r = requests.post(endpoint,
                      data={'m':m,'ts':time.time(),'src':nodeid},
                      auth=auth)
    return r.text


if '__main__' == __name__:
    import sys
    sys.path.append(expanduser('~'))
    from cred import cred

    M = []
    if len(sys.argv) == 1:
        print('No argument supplied. Sending own IPs.')
        M.append(json.dumps(getIP(),separators=(',',':')))
    else:
        M = sys.argv[1:]

    for m in M:
        print(post5(m,url,('uhcm',cred['uhcm'])))
