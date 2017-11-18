import unittest,sys
from os.path import expanduser,exists
sys.path.append(expanduser('~'))


class TestStorage(unittest.TestCase):

    def test_storage2(self):
        from node.storage.storage2 import storage
        store = storage()
        tables = store.get_list_of_tables()
        self.assertTrue(len(tables) >= 73)
        for table in tables:
            columns = store.get_list_of_columns(table)
            self.assertTrue(len(columns) >= 2)              # at least a time and a value
            self.assertTrue('ReceptionTime' in columns)     # all value must have ReceptionTime

    '''def test_storage(self):
        from node.storage.storage import storage_read_only
        dbfile = '/var/uhcm/incoming/base-003/storage/sensor_data.db'
        if not exists(dbfile):
            return True
        s = storage_read_only(dbfile=dbfile)
        r = s.read_latest_non_null('node-008','ReceptionTime','d2w')
        #print r
        #self.assertTrue(parse_SeaFET(m) is not None)'''


if __name__ == '__main__':
    unittest.main()
