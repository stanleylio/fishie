import unittest,sys
sys.path.append('/home/nuc/node')
from helper import ts2dt,dt2ts,get_dbfile


class TestHelper(unittest.TestCase):

    def test_dtts(self):
        from datetime import datetime
        dt = datetime.utcnow()
        self.assertEqual(ts2dt(dt2ts(dt)),dt)


if __name__ == '__main__':
    unittest.main()
