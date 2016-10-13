# authentication stuff for the kmet-bbb otg-met link
# TODO: update the UHCM base-004 i7NUC link to use this instead of rq5
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2016
import base64
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA


def get_signature(m,k):
    h = SHA512.new(m)
    key = RSA.importKey(k)
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(h)
    return base64.b64encode(signature)

def validate_message(m,sig,publickey):
    sig = base64.b64decode(sig)
    publickey = RSA.importKey(publickey)
    verifier = PKCS1_v1_5.new(publickey)
    h = SHA512.new(m)
    return verifier.verify(h,sig)


if '__main__' == __name__:
    #key = open('/home/nuc/.ssh/id_rsa').read()
    #from config import node
    #key = open(node.private_key_file).read()
    privatekey = open('id_rsa').read()
    publickey = open('id_rsa.pub').read()

    m = 'memento mori'
    assert validate_message(m,get_signature(m,privatekey),publickey)
