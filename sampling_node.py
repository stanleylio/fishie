#!/usr/bin/python
#
# logging script for sensor node
#
# Stanley Hou In Lio, stanleylio@gmail.com
# All Rights Reserved. October 2015
import serial,sys,time,traceback,importlib
import config,drivers,storage
import Adafruit_BBIO.UART as UART
from datetime import datetime,timedelta
from os import makedirs
from os.path import exists
from z import send,get_action
from storage.storage import storage
from config.config_support import *
from parse_support import pretty_print
from random import randint
from drivers.indicators import *

node = importlib.import_module('node_{:03d}'.format(get_node_id()))

if not is_node():
    print('Not configured as a sensor node (see node_config.ini). Terminating.')
    sys.exit()

try:
    UART.setup('UART1')
    UART.setup('UART2')
    UART.setup('UART3')
    UART.setup('UART4')
except:
    pass

import sampling_core

def PRINT(s):
    #pass
    print(s)

def dt2ts(dt):
    return time.mktime(dt.timetuple()) +\
                 (dt.microsecond)*(1e-6)

def log(f,line):
    ts = datetime.utcnow()
    f.write('{}\t{}\n'.format(ts.isoformat(),line.strip()))
    f.flush()

store = storage({node.id:read_capabilities()[node.id]})

# wait at most 1 minute for the system clock to initialize (ntpdate, hwclock, GPS etc.)
last_sampled = store.read_last_N(get_node_id(),'Timestamp')
if last_sampled is not None:
    last_sampled = last_sampled['Timestamp'][0]
d = datetime.now()
count = 0

while True:
    if last_sampled is None:
        break
    if d > last_sampled:
        break
    #if last_sampled is None and d.year >= 2015 and d.month >= 10:   # evil hack-ish heristics
    #    break
    if count > 60:
        break
    PRINT('waiting for system clock...')
    d = datetime.now()
    count = count + 1
    time.sleep(1)

log_dir = node.log_dir
if not exists(log_dir):
    makedirs(log_dir)
event = open(join(log_dir,'capture.log'),'a+',0)
def log_event(line):
    PRINT(line)
    log(event,line)

indicators_setup()

try:
    multi_sample = node.multi_sample    # take multiple readings per period
except:
    multi_sample = 1


with serial.Serial(node.xbee_port,node.xbee_baud,timeout=1) as s,\
     open(join(log_dir,'capture.log'),'a+',0) as event:
    try:
        log_event('begin sampling')
        
        last_sampled = datetime.utcnow() + timedelta(days=-1)
        last_blinked = datetime.utcnow() + timedelta(days=-1)
        dither = 0
        
        while True:
            # process incoming commands
            line = s.readline()
            tmp = get_action(line)
            if tmp is not None and ('do sample' == tmp['action']):
                requester = tmp['from']
            else:
                requester = None

            scheduled = (datetime.utcnow() - last_sampled) >= timedelta(seconds=node.wait + dither)
            requested = requester is not None

            if scheduled or requested:
                for i in range(multi_sample):
                    time.sleep(0.1)
                    
                    red_on()
                    usr0_on()
                    
                    d = sampling_core.sampling_core(log_event)

                    red_off()
                    usr0_off()

                    pretty_print(d)

                    store.write(node.id,d)

                    # JSON/serial likes POSIX
                    # SQLite likes python datetime
                    # pretty_print() now takes both
                    d['Timestamp'] = dt2ts(d['Timestamp'])
                    tmp = {c['comtag']:d[c['dbtag']] for c in node.conf}
                    if scheduled:
                        # if this is just a regular scheduled broadcast
                        send(s,tmp)
                        time.sleep(0.2)
                    elif requested:
                        # if this is a response to a specific request
                        send(s,tmp,dest=requester)
                        requester = None
                        break

                last_sampled = datetime.utcnow()
                dither = randint(0,100)/10.

            if (datetime.utcnow() - last_blinked) >= timedelta(seconds=1):
                usr3_on()
                green_on()
                time.sleep(0.01)
                usr3_off()
                green_off()
                last_blinked = datetime.utcnow()

    except KeyboardInterrupt:
        log_event('user interrupted')
        
    indicators_cleanup()
    log_event('terminated')

