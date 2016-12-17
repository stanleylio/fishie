import unittest,sys
from os.path import expanduser
sys.path.append(expanduser('~'))
from node.storage.storage2 import storage_read_only


class TestStorage2(unittest.TestCase):

    def test_read_latest_non_null(self):
        s = storage_read_only()
        print s.read_latest_non_null('node-022','ReceptionTime','ticker')
        #self.assertTrue(parse_SeaFET(m) is not None)

    def test_read_last_N_minutes(self):
        s = storage_read_only()
        print s.read_last_N_minutes('node-007','ReceptionTime',1,'T_280')


if __name__ == '__main__':
    unittest.main()
