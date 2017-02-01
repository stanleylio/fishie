import unittest,sys
from os.path import expanduser
sys.path.append(expanduser('~'))
from node.parse_support import parse_message,pretty_print


M_poh = [
    #'{"from":"node-001","payload":{"C2Amp":1584.3,"T_180":31.9,"T_4330f":27.322,"sal":0.0,"T_5803":27.9,"TCPhase":61.071,"ts":1478741586.279009,"ec":0.0,"Air":-14.915,"C2RPh":4.219,"P_180":101534,"P_5803":109.39,"C1RPh":65.29,"CalPhase":73.904,"C1Amp":2182.3,"RawTemp":-17.9,"O2":-36.845}}726535d6',
    'node-003,R,2016-11-02 01:47:14,102.05,24.66,251.400,99.415,26.080,82.988,25.536,3055,4130,b3844b99',
    '{"from":"node-004","payload":{"C2Amp":1180.9,"T_180":34.7,"T_4330f":36.386,"sal":0.0,"T_5803":34.69,"TCPhase":27.952,"ts":1444958592.790913,"ec":7.28,"Air":90.86,"C2RPh":4.402,"P_180":101664,"P_5803":101.57,"C1RPh":32.354,"CalPhase":25.823,"C1Amp":702.4,"RawTemp":-295.9,"O2":192.554}}e002b5aa',
    '{"from":"node-007","payload":{"T_180":33.1,"Amb_Si1145":986,"ts":1478741544.859069,"T_280":28.176,"Wind_avg":1.18,"P_180":101679,"IR_Si1145":7630,"P_280":101.477,"RH_280":70.828,"UV_Si1145":306,"Wind_gust":1.44}}602df8df',
    'us2,477714,0850,4090',
    'us1,496408,0821,5879',
    'kph1,28884,128,4331700,4331442,4331440,3.219,4.376',
    'SATPHA0371,2016315,1.7644902,7.95901,8.00000,25.9261,25.7465,34.3853,4.900,nan,-0.97667903,-0.92524648,0.72758228,9.654,41,23.0,4.947,9.558,6.176,5.753,165,10,0.00000000,0x0000,246',
    'kph2,27897,23,4181400,4181245,4181243,3.243,4.215',
    'SATPHA0358,2016315,1.7657024,8.06813,8.05069,26.3579,26.4097,34.8719,5.841,nan,-0.93000263,-0.88204473,0.71785599,9.904,37,21.5,4.915,9.784,6.162,5.522,0,10,0.00000000,0x0000,89',
    '<?xml version="1.0"?><datapacket><hdr><mfg>Sea-Bird</mfg><model>16plus</model><sn>01607354</sn></hdr><data><t1> 26.9123</t1><c1> 0.00004</c1><p1>   0.069</p1><v0>0.0319</v0><sal>  0.0126</sal><dt>2016-06-17T02:28:35</dt></data></datapacket>',
    '#<?xml version="1.0"?><datapacket><hdr><mfg>Sea-Bird</mfg><model>16plus</model><sn>01607354</sn></hdr><data><t1> 29.1153</t1><c1> 0.00005</c1><p1>   0.009</p1><v0>0.0147</v0><sal>  0.0133</sal><dt>2017-01-06T23:58:33</dt><dens> -4.0773</dens><vb>10.6</vb><i> 28.2</i></data></datapacket>',
    '#<?xml version="1.0"?><datapacket><hdr><mfg>Sea-Bird</mfg><model>16plus</model><sn>01607354</sn></hdr><data><t1> 32.2707</t1><c1> 0.00005</c1><p1>   0.009</p1><v0>0.0158</v0><sal>  0.0143</sal><dt>2017-01-07T00:28:03</dt><dens> -5.0482</dens><vb>10.5</vb><i> 27.7</i></data></datapacket>',
    'seabird1,9,0,1800,1353,1351,3.207,4.497',
    '#<?xml version=\"1.0\"?><datapacket><hdr><mfg>Sea-Bird</mfg><model>16plus</model><sn>01607354</sn></hdr><data><t1> 25.0142</t1><c1> 4.13692</c1><p1>   0.235</p1><v0>0.1691</v0><sal> 26.4830</sal><dt>2017-01-07T01:56:33</dt><dens> 16.9152</dens><vb>10.7</vb><i> 28.3</i></data></datapacket>',
    'seabird1,46,0,9900,9606,9604,3.203,4.508',
    '{"from":"node-013","payload":{"d2w":1148.2,"VbattV":4.024,"ticker":12}}4b71f103',
]


class TestParse(unittest.TestCase):

    def test_parse_message(self):
        for m in M_poh:
            m = parse_message(m)
            self.assertTrue(m is not None)

    def test_pretty_print(self):
        for m in M_poh:
#            pretty_print(parse_message(m))
            pass


if __name__ == '__main__':
    unittest.main()
