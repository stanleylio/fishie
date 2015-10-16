#!/usr/bin/python
import serial,sys,json,time,socket
sys.path.append('config')
from datetime import datetime,timedelta
from z import get_checksum
from config_support import *
from parse_support import parse_message,pretty_print

from_tag = socket.gethostname()

node_id = int(from_tag[5:8])
exec('import base_{:03d} as base'.format(node_id))

with serial.Serial(base.xbee_port,base.xbee_baud,timeout=1) as s:
    
    #to_tag = 'node-004'

    while True:

        print
        print '= = = = ='
        node_id = int(raw_input('\nEnter node ID to request sample from...'))
        to_tag = 'node-{:03d}'.format(node_id)
        
        tmp = {}
        tmp['action'] = 'do sample'
        tmp = {'from':from_tag,'to':to_tag,'payload':tmp}
        tmp = json.dumps(tmp,separators=(',',':'))
        tmp = '{}{}\n'.format(tmp,get_checksum(tmp))
        print 'Command:'
        print tmp
        s.flushInput()
        s.flushOutput()
        s.write(tmp)

        print 'Response:'
        for i in range(5):
            line = s.readline()
            if len(line) > 0:
                line = line.strip()
                print line
                d = parse_message(line)
                #print d
                if d is not None and node_id == d['node-id']:
                    pretty_print(d)
                    break
        
        s.flushInput()
        s.flushOutput()


