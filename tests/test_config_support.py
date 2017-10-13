# python -m unittest discover
import unittest,sys
from os.path import expanduser,exists
sys.path.append(expanduser('~'))
from node.config.config_support import config_as_dict,get_list_of_nodes,get_list_of_disp_vars,\
     get_list_of_variables,get_list_of_devices,get_config


class TestConfig(unittest.TestCase):

    def test_config_as_dict(self):
        C = config_as_dict()
        self.assertTrue('poh' in C.keys())
        
        for site in sorted(C.keys()):
            self.assertTrue(len(C[site]) > 0)

    def test_get_list_of_nodes(self):
        c = config_as_dict()
        for site in sorted(c.keys()):
            if site not in ['poh','makaipier','coconut','sf','uhm']:
                continue
            self.assertTrue(len(get_list_of_nodes(site)) > 0)   # site must have at least one node
            self.assertTrue(set(get_list_of_nodes(site)).issubset(set(c[site])))    # optional

    def test_config(self):
        for site in config_as_dict():
            if site not in ['poh','makaipier','coconut','sf','uhm']:
                continue
            for node in get_list_of_nodes(site):
                self.assertTrue(len(get_list_of_variables(node)) > 0)
                self.assertTrue(len(get_list_of_disp_vars(node)) > 0)
                #self.assertTrue(len(get_type(site,node)) > 0)
                #self.assertTrue(len(get_dbfile(site,node)) > 0)

    def test_get_public_key(self):
        from node.config.config_support import get_public_key
        L = []
        for site in config_as_dict():
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
        self.assertTrue(len(set(keys)) == len(keys) and len(keys) > 0)

    def test_get_list_of_variables(self):
        from node.config.config_support import get_list_of_variables
        C = config_as_dict()
        for site in sorted(C.keys()):
            for node in get_list_of_nodes(site):
                self.assertTrue(len(get_list_of_variables(node)) > 0)

    '''def test_get_attr(self):
        from node.config.config_support import get_attr
        for site in sorted(config_as_dict().keys()):
            for node in get_list_of_nodes(site):
                self.assertTrue(get_attr(node,'name') is not None)
                self.assertTrue(get_attr(node,'location') is not None)
                self.assertTrue(get_attr(node,'note') is not None)'''

    '''def test_get_config(self):
        from node.config.config_support import get_config
        for site in sorted(config_as_dict().keys()):
            for node in get_list_of_nodes(site):
                for var in get_list_of_variables(node):
                    #print(node,var,get_config('plot_range',node,variable_name=var,default=0))
                    pass'''

    def test_get_unit(self):
        from node.config.config_support import get_unit
        for site in sorted(config_as_dict().keys()):
            for node in get_list_of_nodes(site):
                for var in get_list_of_variables(node):
                    self.assertTrue(get_unit(node,var) is not None)

    def test_get_range(self):
        from node.config.config_support import get_range
        for site in sorted(config_as_dict().keys()):
            for node in get_list_of_nodes(site):
                for var in get_list_of_variables(node):
                    r = get_range(node,var)
                    self.assertTrue(r[0] < r[1])

    def test_get_interval(self):
        from node.config.config_support import get_interval
        for site in sorted(config_as_dict().keys()):
            for node in get_list_of_nodes(site):
                for var in get_list_of_variables(node):
                    self.assertTrue(get_interval(node,var) > 0)
                    

if __name__ == '__main__':
    unittest.main()
