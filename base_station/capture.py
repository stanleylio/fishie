#!/usr/bin/python
#
# ID the messages received from serial port, and parse them.
# Does NOT write to database - for debugging use
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

import sys,re,serial,io,time
sys.path.append('storage')
import Adafruit_BBIO.UART as UART
from datetime import datetime
from os.path import join,exists
from os import mkdir
from storage import storage
from config_support import read_config
from parse_support import NodeMessageParser,pretty_print
import traceback


def PRINT(s):
    #pass
    print(s)

def log(f,line):
    ts = datetime.utcnow()
    f.write('{}\t{}\n'.format(ts.isoformat(),line.strip()))
    f.flush()


d = datetime.now()
count = 0
while d.year < 2015 and count < 60:     # heristics, hack-ish
    d = datetime.now()
    count = count + 1
    time.sleep(1)

# read configuration
tmp = read_config()
serial_port = tmp['base']['port']
baud_rate = int(tmp['base']['baud'])
log_dir = tmp['base']['logdir']

unrecognized = 'unrecognized.txt'
logfile = 'capture.log'
if not exists(log_dir):
    mkdir(log_dir)

store = storage()
nmp = NodeMessageParser()

UART.setup('UART1')

with open(join(log_dir,logfile),'a+',0) as event,\
     open(join(log_dir,unrecognized),'a+',0) as unrecognized,\
     open(join(log_dir,'raw.txt'),'w',0) as raw:
    try:
        with serial.Serial(serial_port,baud_rate,timeout=2) as ser:
            log_event = lambda line: log(event,line)
            log_unrecognized = lambda line: log(unrecognized,line)

            log_event('capture begins')

            # not sure about this (s,s,1). The documentation says no.
            # but nothing is being sent from the base station at the moment, so...
            ser.flushInput()
            s = io.TextIOWrapper(io.BufferedRWPair(ser,ser,1),newline=None)
            while True:
                line = ''
                try:
                    line = s.readline()
                    raw.write(line)         # "ding!" for debugging the field base station
                    line = line.strip()
                    if len(line) > 0:
                        d = nmp.parse_message(line)
                        node_id = d['node_id']
                        if node_id is not None:
                            d['ReceptionTime'] = datetime.utcnow()
                            #print 'From node {}: {}'.format(node_id,str(d))
                            #print 'From node {}: {}'.format(node_id,line)
                            pretty_print(d)
                            store.write(node_id,d)
                        else:
                            PRINT('capture: unrecognized node ID (new node?)')
                            log_unrecognized(line)
                except serial.SerialException:
                    PRINT('capture: USB-to-serial converters are EVIL')
                    log_event('USB-to-serial converters are EVIL')
                except UnicodeDecodeError:
                    # random characters from serial line... ignore.
                    pass
                except Exception as e:
                    PRINT('capture: exception')
                    traceback.print_exc()
                    log_unrecognized(line)
                    #raise e
    except KeyboardInterrupt:
        PRINT('capture: user interrupted')
        log_event('user interrupted')

    log_event('capture terminated')

