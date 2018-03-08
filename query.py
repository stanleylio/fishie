import serial, sys, json, time, socket, importlib
from datetime import datetime, timedelta
from os.path import expanduser
sys.path.append(expanduser('~'))
from node.z import get_checksum
from node.config.config_support import *
from node.parse_support import parse_message, pretty_print


def get_request_cmd(node_id):
    if node_id == 'node-003':
        return 'node-003s\r\n'
    else:
        payload = {'action':'do sample',
                   'm':1}
        cmd = {'from':socket.gethostname(),
               'to':node_id,
               'payload':payload}
        cmd = json.dumps(cmd,separators=(',',':'))
        return cmd + get_checksum(cmd) + '\n'
    

if '__main__' == __name__:
    #with serial.Serial(base.xbee_port,base.xbee_baud,timeout=2) as s:
    with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as s:

        if len(sys.argv) <= 1:
            print('Example: python request.py node-003 to query node-003')
            sys.exit()

        IDs = []
        for i in range(1, len(sys.argv)):
            IDs.append(sys.argv[i])

        for node_id in IDs:        
            print('\n= = = = =')
            
            #node_id = int(raw_input('\nEnter node ID to request sample from...'))
            '''to_tag = node_id
            tmp = {}
            tmp['action'] = 'do sample'
            tmp['m'] = 1    # multi_sample
            tmp = {'from':from_tag,'to':to_tag,'payload':tmp}
            tmp = json.dumps(tmp,separators=(',',':'))
            tmp = '{}{}\n'.format(tmp,get_checksum(tmp))'''

            tmp = get_request_cmd(node_id)
            print('Command:')
            print(tmp)
            s.flushInput()
            s.flushOutput()
            s.write(tmp)

            continue
            
            '''print 'Listening...'
            for i in range(10):
                line = s.readline()
                if len(line) > 0:
                    line = line.strip()
                    print line
                    d = parse_message(line)
                    #print d
                    if d is not None and node_id == d['node-id']:
                        pretty_print(d)
                        break
                else:
                    print '(silence...)'
            
            s.flushInput()
            s.flushOutput()'''
