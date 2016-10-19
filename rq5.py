# Experimental real-time POST to i7 server
# superceded by send2server
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# June 2016
import requests
import base64
from datetime import datetime
from helper import *
from config.config_support import get_node_tag
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA


#key = open('/home/nuc/.ssh/id_rsa').read()
from config import node
key = open(node.private_key_file).read()

myid = get_node_tag()


def get_signature(m,k):
    h = SHA512.new(m)
    key = RSA.importKey(k)
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(h)
    return signature

def sign(m):
    signature = get_signature(m,key)
    signature = base64.b64encode(signature)
    return {'m':m,'s':signature,'ts':dt2ts(datetime.utcnow())}

def send_to_server(m):
    # dump to txt
    #hosturl = 'http://grogdata.soest.hawaii.edu/poh/api/s1/submit'
    # write to db
    #hosturl = 'http://grogdata.soest.hawaii.edu/poh/api/s2/submit'
    hosturl = 'http://grogdata.soest.hawaii.edu/poh/api/s3/submit'
    d = sign(m)
    params = {'client':myid}
    return requests.post(hosturl,params=params,data=d)


if '__main__' == __name__:
    #r = send_to_server("Millions long for immortality who don't know what to do with themselves on a rainy Sunday afternoon.")
    #r = send_to_server('{"node":"node-008","ReceptionTime":1466317265.849019,"VbattmV":4026}')
    #r = send_to_server('us2,169663,0828,4046')
    #print format_and_sign('haha')
    #print format_and_sign({'ReceptionTime':None,'Timestamp':str(datetime.utcnow()),'P_5803':123.456})

    r = send_to_server('memento mori')
    print 'server\'s response:'
    print r.text

