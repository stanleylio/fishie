import re
from ConfigParser import RawConfigParser
from os.path import exists

def read_config(filename='node_config.ini',pattern='.*'):
    if exists(filename):
        parser = RawConfigParser(allow_no_value=True)
        parser.read(filename)

        config = {}
        for s in parser.sections():
            if re.match(pattern,s):
                config[s] = dict(parser.items(s))
        return config
    else:
        raise IOError('read_config(): {} not found'.format(filename));

if '__main__' == __name__:
    print read_config('node_config.ini')
    
