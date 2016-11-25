import unittest,sys
sys.path.append('/home/nuc/node')
from authstuff import get_signature,validate_message


class TestSeafet(unittest.TestCase):

    def test_sign(self):
        import string,random
        from os.path import expanduser
        privatekey = open(expanduser('~/.ssh/id_rsa')).read()
        publickey = open(expanduser('~/.ssh/id_rsa.pub')).read()

        for i in range(100):
            N = random.randint(1,250)
            m = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))
            self.assertTrue(validate_message(m,get_signature(m,privatekey),publickey))


if __name__ == '__main__':
    unittest.main()
