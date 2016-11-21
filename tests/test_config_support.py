import sys
sys.path.append('/home/nuc/node')   # ... but absolute path is cheating!
from config.config_support import config_as_dict,get_list_of_nodes


c = config_as_dict()
for k in sorted(c.keys()):
    print k
    print '\t',','.join(c[k])


print

print get_list_of_nodes('')
