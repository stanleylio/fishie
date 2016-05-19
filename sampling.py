#!/usr/bin/python
#
# script dispatcher
#
# Stanley Hou In Lio, stanleylio@gmail.com
# All Rights Reserved. October 2015
import importlib
import config
from config.config_support import *
import sys


if is_node():
    import sampling_node
elif is_base():
    import sampling_base
else:
    print('neither a sensor node nor a base station. exit()')
    sys.exit()
