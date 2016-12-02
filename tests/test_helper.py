import unittest,sys
from os.path import expanduser
sys.path.append(expanduser('~/node'))
from helper import ts2dt,dt2ts


class TestHelper(unittest.TestCase):

    def test_dtts(self):
        from datetime import datetime
        dt = datetime.utcnow()
        self.assertEqual(ts2dt(dt2ts(dt)),dt)


if __name__ == '__main__':
    unittest.main()
