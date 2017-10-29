# python -m unittest discover
import unittest,sys
from os.path import expanduser,exists
sys.path.append(expanduser('~'))
from node.config.config_support import get_config,\
     get_list_of_sites,get_list_of_nodes,get_list_of_variables,get_list_of_disp_vars,\
     get_unit,get_description


class TestConfig(unittest.TestCase):

    def test_config(self):
        for site in sorted(get_list_of_sites()):
            for node in get_list_of_nodes(site):
                self.assertTrue(len(get_list_of_variables(node)) > 0)
                self.assertTrue(len(get_list_of_disp_vars(node)) > 0)
                for var in get_list_of_disp_vars(node):
                    self.assertTrue(get_unit(node,var) is not None)
                    self.assertTrue(type(get_description(node,var)) is str)
                  

if __name__ == '__main__':
    unittest.main()
