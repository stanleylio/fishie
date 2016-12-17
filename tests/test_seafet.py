import unittest,sys
from os.path import expanduser
sys.path.append(expanduser('~'))
from node.drivers.seafet import parse_SeaFET


class TestSeafet(unittest.TestCase):

    def test_parse_SeaFET(self):
        M = ['SATPHA0371,2016306,8.2669678,7.96194,7.99229,24.4627,24.2046,34.2334,4.413,nan,-0.97720563,-0.92704624,0.76134235,9.847,40,22.1,4.939,9.752,6.175,5.780,298,10,0.00000000,0x0000,229',
             'SATPHA0358,2016345,22.0146484,8.04703,8.00464,24.6224,24.5918,34.3269,5.195,nan,-0.93211651,-0.88638008,0.75759977,8.945,40,23.8,4.915,8.833,6.162,5.438,184,10,0.00000000,0x0000,192',
             'kph1,46547,289,6980400,6980378,6980376,3.191,4.262',
             'kph2,27897,23,4181400,4181245,4181243,3.243,4.215']
        for m in M:
            #print
            #print parse_SeaFET(m).keys()
            self.assertTrue(parse_SeaFET(m) is not None)


if __name__ == '__main__':
    unittest.main()
