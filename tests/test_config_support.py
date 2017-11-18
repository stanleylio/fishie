# python -m unittest discover
import unittest,sys
from os.path import expanduser,exists
sys.path.append(expanduser('~'))
from node.config.config_support import get_list_of_nodes,get_list_of_disp_vars,\
     get_list_of_variables,get_list_of_devices,get_description,get_list_of_sites


class TestConfig(unittest.TestCase):

    def test_get_list_of_nodes(self):
        sites = sorted(get_list_of_sites())
        self.assertTrue('poh' in sites)     # that much I'm sure
        for site in sites:
            self.assertTrue(len(get_list_of_devices(site)) > 0)   # site should have at least one device

    '''def test_get_public_key(self):
        from node.config.config_support import get_public_key
        L = []
        for site in sorted(get_list_of_sites()):
            for node in sorted(get_list_of_devices(site)):
                L.append((node,get_public_key(node)))

        # Servers, base stations, and KM's should have public keys
        # for sensor nodes that's optional.
        L = dict(L)
        keys = []
        for k,v in L.items():
            #print k
            self.assertTrue(v is not None if k.startswith('base-') else True)
            self.assertTrue(v is not None if k.startswith('kmet-') else True)
            self.assertTrue(v is not None if k.startswith('glazerlab-') else True)
            keys.append(get_public_key(k))

        # No duplicate keys (for those that have a key)
        keys = filter(lambda x: x is not None,keys)
        self.assertTrue(len(set(keys)) == len(keys) and len(keys) > 0)'''

    def test_get_description(self):
        from node.config.config_support import get_description
        for site in sorted(get_list_of_sites()):
            for node in get_list_of_nodes(site):
                for var in get_list_of_variables(node):
                    self.assertTrue(type(get_description(node,var)) is str)

    def test_get_list_of_variables(self):
        from node.config.config_support import get_list_of_variables
        for site in sorted(get_list_of_sites()):
            for node in get_list_of_nodes(site):
                self.assertTrue(len(get_list_of_variables(node)) > 0)

    def test_get_unit(self):
        from node.config.config_support import get_unit
        for site in sorted(get_list_of_sites()):
            for node in get_list_of_nodes(site):
                for var in get_list_of_variables(node):
                    self.assertTrue(get_unit(node,var) is not None)

    def test_get_range(self):
        from node.config.config_support import get_range
        for site in sorted(get_list_of_sites()):
            for node in get_list_of_nodes(site):
                for var in get_list_of_variables(node):
                    r = get_range(node,var)
                    self.assertTrue(r[0] < r[1])

    def test_get_interval(self):
        from node.config.config_support import get_interval
        for site in sorted(get_list_of_sites()):
            for node in get_list_of_nodes(site):
                for var in get_list_of_variables(node):
                    self.assertTrue(get_interval(node,var) > 0)
                    

if __name__ == '__main__':
    unittest.main()
