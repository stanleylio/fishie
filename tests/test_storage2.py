import unittest,sys
from os.path import expanduser
sys.path.append(expanduser('~'))


class TestStorage2(unittest.TestCase):

    def test_storage2(self):
        from node.storage.storage2 import storage_read_only
        s = storage_read_only()
        print s.read_latest_non_null('node-021','ReceptionTime','Vbatt')
        #self.assertTrue(parse_SeaFET(m) is not None)


if __name__ == '__main__':
    unittest.main()
