import unittest,sys
from os.path import expanduser
sys.path.append(expanduser('~/node'))
from z import get_checksum,check


class TestZ(unittest.TestCase):

    def test_crc(self):
        import string,random

        for i in range(100):
            N = random.randint(1,250)
            m = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))

            self.assertTrue(check('{}{}'.format(m,get_checksum(m))))


if __name__ == '__main__':
    unittest.main()
