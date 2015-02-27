import re
from ConfigParser import RawConfigParser

def read_config(filename,pattern='.*'):
    parser = RawConfigParser(allow_no_value=True)
    parser.read(filename)

    config = {}
    for s in parser.sections():
        if re.match(pattern,s):
            config[s] = dict(parser.items(s))
    return config

