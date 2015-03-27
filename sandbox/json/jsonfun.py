import json
from config_support import read_config

tmp = read_config()
print tmp['node']
print json.dumps(tmp['node'],separators=(',',':'))


#print tmp['node_004']
#print json.dumps(tmp['node_004'])


t = [1,'2',[3,4.4]]
print t
print json.dumps(t,separators=(',',':'))
print json.loads(json.dumps(t,separators=(',',':')))


print json.loads('-Infinity')


