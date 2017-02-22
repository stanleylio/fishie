import unittest,sys
from os.path import expanduser
sys.path.append(expanduser('~'))
from node.drivers.seabird import parse_Seabird


class TestSeabird(unittest.TestCase):

    def test_parse_Seabird(self):
        M = ['<?xml version="1.0"?><datapacket><hdr><mfg>Sea-Bird</mfg><model>16plus</model><sn>01607354</sn></hdr><data><t1> 22.6458</t1><c1> 0.00005</c1><p1>   0.036</p1><v0>0.0148</v0><sal>  0.0110</sal><dt>2016-06-16T04:12:18</dt></data></datapacket>',
             '<?xml version="1.0"?><datapacket><hdr><mfg>Sea-Bird</mfg><model>16plus</model><sn>01607354</sn></hdr><data><t1> 26.9123</t1><c1> 0.00004</c1><p1>   0.069</p1><v0>0.0319</v0><sal>  0.0126</sal><dt>2016-06-17T02:28:35</dt></data></datapacket>',
             'seabird1,36,4.169',
             'seabird1,9,0,1800,1353,1351,3.207,4.497',]
        for m in M:
            #print
            #print parse_SeaFET(m).keys()
            self.assertTrue(parse_Seabird(m) is not None)


if __name__ == '__main__':
    unittest.main()
