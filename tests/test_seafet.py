import unittest,sys
from os.path import expanduser
sys.path.append(expanduser('~/node'))
from drivers.seafet import parse_SeaFET


class TestSeafet(unittest.TestCase):

    def test_parse_SeaFET(self):
        M = ['SATPHA0371,2016306,8.2669678,7.96194,7.99229,24.4627,24.2046,34.2334,4.413,nan,-0.97720563,-0.92704624,0.76134235,9.847,40,22.1,4.939,9.752,6.175,5.780,298,10,0.00000000,0x0000,229',
             'kph2,27897,23,4181400,4181245,4181243,3.243,4.215']
        for m in M:
            self.assertTrue(parse_SeaFET(m) is not None)


if __name__ == '__main__':
    unittest.main()
