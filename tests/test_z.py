import unittest,sys
from os.path import expanduser
sys.path.append(expanduser('~'))


class TestZ(unittest.TestCase):

    def test_crc(self):
        from node.z import get_checksum,check
        import string,random

        for i in range(100):
            N = random.randint(1,250)
            m = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))

            self.assertTrue(check('{}{}'.format(m,get_checksum(m))))

    def test_get_action(self):
        from node.query import get_request_cmd
        from node.z import get_action

        nodes = ['node-001','node-002','node-004','node-007']
        for node in nodes:
            r = get_request_cmd(node)
            a = get_action(r,_test_myid=node)  # hum...
            #print
            #print node,r,a
            self.assertTrue(a['action'] == 'do sample')


if __name__ == '__main__':
    unittest.main()
