# Communication support functions
#
# Some of them are utils (CRC), others are app-specific (how to append checksum to message)
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2016
import struct, json, re, traceback, logging
from socket import gethostname
from zlib import crc32
# see also: hashlib


def get_checksum(s):
    return '{:08x}'.format(crc32(s.encode()) & 0xffffffff)  # python2-safe?

def check(s):
    try:
        return get_checksum(s[:-8]) == s[-8:]
    except:
        logging.debug(traceback.format_exc())
        logging.debug(s)
        return False

def get_action(line, _test_myid=None):
    """Get the action from a potential command.
Also checks: 1. checksum and 2. whether this is the recipient."""
    try:
        line = line.strip()
        if not check(line):
            logging.debug('checksum failure')
            return

        line = line[:-8]    # discard the checksum and retain the message
        tmp = json.loads(line)
        #print tmp['from']
        #print tmp['to']
        if _test_myid is None:
            _test_myid = gethostname()
        if not tmp.get('to',None) == _test_myid:
            # message not intended for me
            logging.debug('message not intended for this node')
            print('message not intended for {}'.format(_test_myid))
            return

        if 'action' not in tmp['payload']:
            # "action" is mandatory
            logging.debug('no action defined')
            return
        
        d = {}
        d['action'] = tmp['payload']['action']

        '''# "m" (sample count) is obsolete
        # ... time for Google Protocol Buffer?
        try:
            d['multi_sample'] = max(1,tmp['payload']['m'])
        except:
            pass'''

        d['from'] = tmp.get('from',None)
        return d
    except:
        logging.debug(traceback.format_exc())
    return None

def send(channel, sample, src=None, dest=None):
    if src is None:
        src = gethostname()
    tmp = {'from':src,
           'v':1,
           'payload':sample}
    if dest is not None:
        tmp['to'] = dest
    tmp = json.dumps(tmp,separators=(',', ':'))
    m = '{}{}\n'.format(tmp, get_checksum(tmp))
    m = m.encode()
    if channel is not None:
        channel.write(m)
    return m


if '__main__' == __name__:
    logging.basicConfig(level=logging.DEBUG)
    
    #s = 'node_011,1423219154.21,0.0,0.0,3374.18,1012.95,24.1'
    #s = 'node_011,142329154.21,0.0,0.0,3374.18,1012.95,24.1'
    s1 = 'node_011,1423222524.47,0.0,0.0,3245.85,1012.54,24.1,eb9f0088'
    s2 = 'node_004,1428688767.014666,0.0,0.0,3.76,14.0,-55.1,101125,25.4,102.4,25.31,4,540,267,df375a77'
    s3 = 'node_004,1428688771.165071,0.0,0.0,3.77,14.0,-54.5,101126,25.4,102.44,25.31,10,540,281,c5e55b3d'
    s4 = '{"from":"node_004","payload":{"Temp_MS5803":25.51,"Pressure_BMP180":101124,"Amb_Si1145":283,"EZO_ORP":-42.3,"EZO_DO":3.87,"Pressure_MS5803":102.43,"IR_Si1145":510,"Timestamp":1428689419.189611,"EZO_pH":14.0,"EZO_Sal":0.0,"Temp_BMP180":25.6,"EZO_EC":0.0,"UV_Si1145":11}}328712c1'
    s5 = '{"from":"node_004","payload":{"Temp_MS5803":25.64,"Pressure_BMP180":101119,"Amb_Si1145":288,"EZO_ORP":-27.0,"EZO_DO":3.99,"Pressure_MS5803":102.42,"IR_Si1145":520,"Timestamp":1428690057.49952,"EZO_pH":14.0,"EZO_Sal":0.0,"Temp_BMP180":25.8,"EZO_EC":0.0,"UV_Si1145":13}}d6a891c9'
    s6 = '{"from":"node_004","payload":{"Temp_MS5803":25.65,"Pressure_BMP180":101117,"Amb_Si1145":287,"EZO_ORP":-26.7,"EZO_DO":3.99,"Pressure_MS5803":102.4,"IR_Si1145":532,"Timestamp":1428690061.93023,"EZO_pH":14.0,"EZO_Sal":0.0,"Temp_BMP180":25.8,"EZO_EC":0.0,"UV_Si1145":13}}f717a449'
    s7 = '{"to":"base","from":"node_003","payload":{"Thermistor_FLNTU":537,"Temp_MS5803":22.54,"C2Amp_4330f":842.6,"O2Concentration_4330f":272.596,"C1RPh_4330f":34.228,"Chlorophyll_FLNTU":3320,"Pressure_MS5803":80.4mp_4330f":227.0,"AirSaturation_4330f":100.092,"Turbidity_FLNTU":4121,"Timestamp":1441671401.039086,"Temperature_4330f":22.067,"C1Amp_4330f":872.1,"CalPhase_4330f":27.253,"TCPhase_4330f":30.331,"C2RPh_4330f":3.897}}aa6efc3c'
    s8 = '{"to":"base","from":"node_004","payload":{"Timestamp":1443306205.462585,"EZO_EC":4.45}}d74a14c8'

    print(check(s7))


