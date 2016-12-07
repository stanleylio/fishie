import unittest,sys
from os.path import expanduser,exists
sys.path.append(expanduser('~'))
from node.config.config_support import config_as_dict,get_list_of_nodes,get_dbfile,\
     get_tag,get_type,get_dbfile,get_schema


class TestConfig(unittest.TestCase):

    def test_config_as_dict(self):
        c = config_as_dict()
        self.assertTrue('poh' in c.keys())
        
        for site in sorted(c.keys()):
            self.assertTrue(len(c[site]) > 0)

    def test_get_list_of_nodes(self):
        c = config_as_dict()
        for site in sorted(c.keys()):
            self.assertTrue(len(get_list_of_nodes(site)) > 0)   # site must have at least one node
            self.assertTrue(set(get_list_of_nodes(site)).issubset(set(c[site])))    # optional

    def test_config(self):
        for site in config_as_dict():
            self.assertTrue(len(get_schema(site)) > 0)
            for node in get_list_of_nodes(site):
                self.assertTrue(len(get_tag(site,node)) > 0)
                self.assertTrue(len(get_type(site,node)) > 0)
                self.assertTrue(len(get_dbfile(site,node)) > 0)

    def test_get_dbfile(self):
        """every node must have a data_source defined; all sqlite data_source must exists"""
        c = config_as_dict()
        for site in sorted(c.keys()):
            for node in get_list_of_nodes(site):
                dbfile = get_dbfile(site,node)
                b = 'mysql' in dbfile or exists(dbfile)
                if not b:
                    print(dbfile)
                self.assertTrue(b)

    '''def test_get_dbfile2(self):
        from helper import get_dbfile as oldver
        c = config_as_dict()
        for site in sorted(c.keys()):
            for node in get_list_of_nodes(site):
                new = get_dbfile(site,node)
                old = oldver(site,node)
                #print new,old
                if 'mysql' not in new:
                    self.assertEqual(new,old)'''

            
if __name__ == '__main__':
    unittest.main()
