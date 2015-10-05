#!/usr/bin/python
import serial,sys,json,time,socket
sys.path.append('config')
from datetime import datetime,timedelta
from z import get_checksum
from config_support import *
from parse_support import parse_message,pretty_print

xbee_port = get_xbee_port()
xbee_baud = get_xbee_baud()

with serial.Serial(xbee_port,xbee_baud,timeout=1) as s:

    from_tag = socket.gethostname()
    #to_tag = 'node_004'

    while True:

        tmp = raw_input('\nEnter node ID to request sample from...')
        to_tag = 'node_{:03d}'.format(int(tmp))
        
        tmp = {}
        tmp['action'] = 'do sample'
        tmp = {'from':from_tag,'to':to_tag,'payload':tmp}
        tmp = json.dumps(tmp,separators=(',',':'))
        s.write('{}{}\n'.format(tmp,get_checksum(tmp)))

        for i in range(3):
            line = s.readline()
            if len(line) > 0:
                line = line.strip()
                print line
                d = parse_message(line)
                if d is not None:
                    pretty_print(d)
                    break


