# experimental real-time POST to i7 server
# this is a temp debug script
#   don't want to copy over base-003's private key, and
#   dev Flask server is not visible publicly
# Stanley Hou In Lio, June 2016
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
#from config import node
#key = open(node.private_key_file).read()

myid = 'thyself'
#myid = get_node_tag()


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

# accept stuff that can be encoded in JSON, not just strings.
# (that's why if you pass 'dict in JSON format' you will need json.loads(json.loads())
# to parse it - this already handle json.dumps() for you.)
def send_to_server(d):
    #hosturl = 'http://grogdata.soest.hawaii.edu/poh/api/s2/submit'
    hosturl = 'http://192.168.0.20:5000/poh/api/s2/submit'
    d = format_and_sign(d)
    params = {'client':myid}
    r = requests.post(hosturl,params=params,data=d)
    return r


if '__main__' == __name__:
    #r = send_to_server("Millions long for immortality who don't know what to do with themselves on a rainy Sunday afternoon.")
    #r = send_to_server('{"node":"node-008","ReceptionTime":1466317265.849019,"VbattmV":4026}')
    #r = send_to_server({"node":"node-004","AirSaturation":109.367,"C2Amp":395.0,"T_5803":28.56,"RawTemp":-56.1,"Temperature":27.769,"C2RPh":4.216,"sal":0.0,"Timestamp":1466321411.256469,"TCPhase":27.785,"ec":4.81,"P_180":101975,"P_5803":106.21,"C1Amp":332.8,"ReceptionTime":1466321405.936751,"C1RPh":32.001,"CalPhase":25.352,"O2Concentration":268.022,"T_180":31.9})
    #r = send_to_server({"temperature_seabird":26.2563,"node":"node-025","dt_seabird":1466325215.0,"v0_seabird":0.2906,"salinity_seabird":18.5024,"pressure_seabird":0.237,"ReceptionTime":1466325219.760848,"sn_seabird":"01607354","conductivity_seabird":3.06515})
    r = send_to_server({"node":"node-025","ReceptionTime":1466325219.760848})
    print 'server\'s response:'
    print r.text

