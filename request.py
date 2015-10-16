#!/usr/bin/python
import serial,sys,json,time,socket,config,importlib
from datetime import datetime,timedelta
from z import get_checksum
from config.config_support import *
from parse_support import parse_message,pretty_print

from_tag = socket.gethostname()
base = importlib.import_module('base_{}'.format(from_tag[5:8]))

with serial.Serial(base.xbee_port,base.xbee_baud,timeout=1) as s:

    if len(sys.argv) > 1:
        node_id = int(sys.argv[1])
    else:
        print('To query node N, python request.py N')
        
    #while True:
    if True:
        print
        print '= = = = ='
        
        #node_id = int(raw_input('\nEnter node ID to request sample from...'))
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

        exit()
        
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


