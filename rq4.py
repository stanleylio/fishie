import requests
import json
import base64
from datetime import datetime
from helper import *
from config.config_support import get_node_tag
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA


key = open('/home/nuc/.ssh/id_rsa').read()

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

def format_and_sign(d):
    return sign(json.dumps(d,separators=(',',':')))

def send_to_server(d):
    hosturl = 'http://grogdata.soest.hawaii.edu/poh/api/s1/submit'
    d = format_and_sign(d)
    params = {'client':myid}
    r = requests.post(hosturl,params=params,data=d)
    return r


if '__main__' == __name__:
    #print format_and_sign('haha')
    #print format_and_sign({'ReceptionTime':None,'Timestamp':str(datetime.utcnow()),'P_5803':123.456})

    r = send_to_server('memento mori')
    print r.text
