import struct,json
from zlib import crc32
# see also: hashlib

# support functions for CRC32 checksum in communication

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015


def PRINT(s):
    #pass
    print(s)

def get_checksum(s):
    return '{:08x}'.format(crc32(s) & 0xffffffff)

# schedule for deletion. error detection script should not be concerned with message format.
def wrap(s):
    return '{},{}'.format(s,get_checksum(s))

# not sure if it's the late nights, the nonstop programming, the coffee
# overdose, or I'm just not cut out for maths and algorithms.
def check(s):
    s = s.strip()
    good = False
    if len(s) > 9:
        try:
            ss = s[:-9]
            cs = s[-8:]
            good = (crc32(ss) & 0xffffffff) == int(cs,16)
        except:
            return False
    else:
        return False
    return good

# that one above is just bad. that comma... should not be part of the msg or be check()'s concern.
# the last 8 characters are the checksum digits
def check2(s):
    s = s.strip()
    try:
        return get_checksum(s[:-8]) == s[-8:]
    except:
        PRINT('check2(): duh')
        return False


if '__main__' == __name__:
    #s = 'node_011,1423219154.21,0.0,0.0,3374.18,1012.95,24.1'
    #s = 'node_011,142329154.21,0.0,0.0,3374.18,1012.95,24.1'
    s1 = 'node_011,1423222524.47,0.0,0.0,3245.85,1012.54,24.1,eb9f0088'
    s2 = 'node_004,1428688767.014666,0.0,0.0,3.76,14.0,-55.1,101125,25.4,102.4,25.31,4,540,267,df375a77'
    s3 = 'node_004,1428688771.165071,0.0,0.0,3.77,14.0,-54.5,101126,25.4,102.44,25.31,10,540,281,c5e55b3d'
    
    #print len(struct.pack('>I',v))
    vcs = wrap(s1)
    print s1
    print vcs

    # corrupting channel...
    #vcs = vcs[:-1]
    #vcs = vcs[:-2]
    #vcs = vcs[:10] + vcs[11:]

    print check(vcs)

    # ARGH I just took the course on this and now I forgot how to do it elegantly.
    # No PhD for me I guess...
    #print
    #print zlib.crc32(s + struct.pack('>I',v)) & 0xffffffff

    print check(s2)
    print check(s3)

    # - - - - -
    print
    s = '{"from":"node_004","payload":{"Temp_MS5803":25.51,"Pressure_BMP180":101124,"Amb_Si1145":283,"EZO_ORP":-42.3,"EZO_DO":3.87,"Pressure_MS5803":102.43,"IR_Si1145":510,"Timestamp":1428689419.189611,"EZO_pH":14.0,"EZO_Sal":0.0,"Temp_BMP180":25.6,"EZO_EC":0.0,"UV_Si1145":11}}328712c1'
    #s = '{"from":"node_004","payload":{"Temp_MS5803":25.64,"Pressure_BMP180":101119,"Amb_Si1145":288,"EZO_ORP":-27.0,"EZO_DO":3.99,"Pressure_MS5803":102.42,"IR_Si1145":520,"Timestamp":1428690057.49952,"EZO_pH":14.0,"EZO_Sal":0.0,"Temp_BMP180":25.8,"EZO_EC":0.0,"UV_Si1145":13}}d6a891c9'
    #s = '{"from":"node_004","payload":{"Temp_MS5803":25.65,"Pressure_BMP180":101117,"Amb_Si1145":287,"EZO_ORP":-26.7,"EZO_DO":3.99,"Pressure_MS5803":102.4,"IR_Si1145":532,"Timestamp":1428690061.93023,"EZO_pH":14.0,"EZO_Sal":0.0,"Temp_BMP180":25.8,"EZO_EC":0.0,"UV_Si1145":13}}f717a449'
    print
    print s
    print check2(s)

    
    


