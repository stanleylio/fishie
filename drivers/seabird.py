# ASSUMPTION: Instrument clock is in UTC
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2016
import xml.etree.ElementTree as ET
from datetime import datetime
import sys,traceback,re
from node.helper import dt2ts


def parse_Seabird(m):
    try:
        if re.match('^seabird\d+.*',m):
            m = m.split(',')
            if 3 == len(m):
                return {'tag':m[0],
                        'ticker':int(m[1]),
                        'Vbatt':float(m[2])}
        else:
            root = ET.fromstring(m)
            if root[0][0].text == 'Sea-Bird' and\
               root[0][1].text == '16plus':
                d = {}
                d['sn'] = root[0][2].text
                for e in root[1]:
                    if not e.tag == 'dt':
                        d[e.tag] = float(e.text.strip())
                    else:
                        d[e.tag] = e.text.strip()
                        d['Timestamp'] = dt2ts(datetime.strptime(e.text.strip(),'%Y-%m-%dT%H:%M:%S'))
                return d
    except:
        #traceback.print_exc()
        pass
    return None


if '__main__' == __name__:
    m = '<?xml version="1.0"?><datapacket><hdr><mfg>Sea-Bird</mfg><model>16plus</model><sn>01607354</sn></hdr><data><t1> 22.6458</t1><c1> 0.00005</c1><p1>   0.036</p1><v0>0.0148</v0><sal>  0.0110</sal><dt>2016-06-16T04:12:18</dt></data></datapacket>'
    print parse_Seabird(m)
    print

    m = '<?xml version="1.0"?><datapacket><hdr><mfg>Sea-Bird</mfg><model>16plus</model><sn>01607354</sn></hdr><data><t1> 26.9123</t1><c1> 0.00004</c1><p1>   0.069</p1><v0>0.0319</v0><sal>  0.0126</sal><dt>2016-06-17T02:28:35</dt></data></datapacket>'
    print parse_Seabird(m)
    print

    m = 'seabird1,36,4.169'
    print parse_Seabird(m)
    
