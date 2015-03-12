import struct
from zlib import crc32
# see also: hashlib

# support functions for CRC32 checksum in communication

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

def get_checksum(s):
    return'{:08x}'.format(crc32(s) & 0xffffffff)

def wrap(s):
    return '{},{}'.format(s,get_checksum(s))

# not sure if it's the late nights, the days of nonstop programming, the coffee
# overdose, or I'm just not cut out for maths and algorithms.
def check(s):
    s = s.strip()
    good = False
    if len(s) > 9:
        try:
            ss = s[:-9]
            cs = s[-8:]
            good = (crc32(ss) & 0xffffffff) == int(cs,16)
            '''if not good:
                print '- - - - -'
                print s
                print crc32(ss)
                print int(cs,16)
                print '- - - - -'
            '''
        except:
            pass
    return good


if '__main__' == __name__:
    #s = 'node_011,1423219154.21,0.0,0.0,3374.18,1012.95,24.1'
    #s = 'node_011,142329154.21,0.0,0.0,3374.18,1012.95,24.1'
    s = 'node_011,1423222524.47,0.0,0.0,3245.85,1012.54,24.1,eb9f0088'
    
    #print len(struct.pack('>I',v))
    vcs = wrap(s)
    print s
    print vcs

    # corrupting channel...
    #vcs = vcs[:-1]     # but this passes...
    #vcs = vcs[:-2]
    #vcs = vcs[:10] + vcs[11:]

    print check(vcs)

    # ARGH I just took the course on this and now I forgot how to do it elegantly.
    # No PhD for me I guess...
    #print
    #print zlib.crc32(s + struct.pack('>I',v)) & 0xffffffff

