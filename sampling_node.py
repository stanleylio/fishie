#!/usr/bin/python
#
# logging script for sensor node
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2016
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
from helper import dt2ts
from socket import gethostname


node_id = gethostname()

import config.node as node
site = node.site
node = importlib.import_module(node.config)


if not is_node():
    print('Not configured as a sensor node (see node_config.ini). Terminating.')
    sys.exit()

# RPi needs no UART.setup()
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

def log(f,line):
    ts = datetime.utcnow()
    f.write('{}\t{}\n'.format(ts.isoformat(),line.strip()))
    f.flush()

# event log and log of received stuff (data and commands alike)
log_dir = node.log_dir
if not exists(log_dir):
    makedirs(log_dir)
event = open(join(log_dir,'capture.log'),'a+',0)
raw = open(join(log_dir,'tsraw.txt'),'a+',0)

def log_event(line):
    PRINT(line)
    log(event,line)

def log_raw(line):
    #PRINT(line)
    log(raw,line)


tmp = get_schema(site)
store = storage('storage/sensor_data.db',schema={node.tag:tmp[node.tag]})

if False:
    # wait at most 1 minute for the system clock to initialize (ntpdate, hwclock, GPS etc.)
    print 'Checking system clock against database...'
    last_sampled = store.read_last_N(get_node_tag(),'Timestamp')
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

indicators_setup()


with serial.Serial(node.xbee_port,node.xbee_baud,timeout=1) as s,\
     open(join(log_dir,'capture.log'),'a+',0) as event:
    try:
        log_event('\nbegin sampling')
        
        last_sampled = datetime.utcnow() + timedelta(days=-1)
        last_blinked = datetime.utcnow() + timedelta(days=-1)
        dither = 0

        try:
            multi_sample = node.multi_sample
        except:
            multi_sample = 1
        
        while True:
            requested = False
            requester = None

            # watch for incoming commands
            line = s.readline()
            if len(line) > 0:
                try:
                    log_raw(line)
                except:
                    traceback.print_exc()
                
                cmd = get_action(line)
                if cmd is not None and ('do sample' == cmd['action']):
                    requested = True
                    requester = cmd.get('from',None)    # shouldn't accept request from anonymous entity...
                    multi_sample = cmd.get('multi_sample',None)

            scheduled = (datetime.utcnow() - last_sampled) >= timedelta(seconds=node.wait + dither)

            if scheduled or requested:
                for i in range(multi_sample):
                    time.sleep(randint(1,5)/10.)
                    
                    red_on()
                    usr0_on()
                    d = sampling_core.sampling_core(log_event)
                    red_off()
                    usr0_off()

                    assert 'node' not in d
                    d['node'] = node_id

                    pretty_print(d)

                    store.write(d)

                    # JSON/serial likes POSIX
                    # SQLite uses python datetime
                    # pretty_print() now takes both
                    d['Timestamp'] = dt2ts(d['Timestamp'])
                    tmp = {c['comtag']:d[c['dbtag']] for c in node.conf}
                    send(s,tmp,dest=requester)

                    last_sampled = datetime.utcnow()

                dither = randint(0,50)/10.

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
