import unittest,sys
from os.path import expanduser,exists
sys.path.append(expanduser('~'))
from node.config.config_support import config_as_dict,get_list_of_nodes,get_dbfile,\
     get_list_of_variables,get_type,get_dbfile,get_schema


class TestConfig(unittest.TestCase):

    def test_config_as_dict(self):
        C = config_as_dict()
        self.assertTrue('poh' in C.keys())
        
        for site in sorted(C.keys()):
            self.assertTrue(len(C[site]) > 0)

    def test_get_list_of_nodes(self):
        c = config_as_dict()
        for site in sorted(c.keys()):
            self.assertTrue(len(get_list_of_nodes(site)) > 0)   # site must have at least one node
            self.assertTrue(set(get_list_of_nodes(site)).issubset(set(c[site])))    # optional

    def test_config(self):
        for site in config_as_dict():
            self.assertTrue(len(get_schema(site)) > 0)
            for node in get_list_of_nodes(site):
                self.assertTrue(len(get_list_of_variables(site,node)) > 0)
                self.assertTrue(len(get_type(site,node)) > 0)
                #self.assertTrue(len(get_dbfile(site,node)) > 0)

    '''def test_get_dbfile(self):
        """every node must have a data_source defined; all sqlite data_source must exists"""
        c = config_as_dict()
        for site in sorted(c.keys()):
            for node in get_list_of_nodes(site):
                dbfile = get_dbfile(site,node)
                b = 'mysql' in dbfile or exists(dbfile)
                if not b:
                    print(dbfile)
                self.assertTrue(b)'''

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

    def test_get_list_of_variables(self):
        from node.config.config_support import get_list_of_variables
        C = config_as_dict()
        for site in sorted(C.keys()):
            for node in get_list_of_nodes(site):
#                print get_list_of_variables(site,node)
                pass

    def test_get_plot_range(self):
        from node.config.config_support import get_plot_range
        c = config_as_dict()
        for site in sorted(c.keys()):
            for node in get_list_of_nodes(site):
                self.assertTrue(get_plot_range(site,node) > 0)

    def test_get_location(self):
        from node.config.config_support import get_location
        c = config_as_dict()
        for site in sorted(c.keys()):
            for node in get_list_of_nodes(site):
                self.assertTrue(get_location(site,node) is not None)

            
if __name__ == '__main__':
    unittest.main()
