#!/usr/bin/python

# ID the messages received from serial port, and parse them.
# Does NOT write to database - for debugging use
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

import sys,re,serial,io,time
sys.path.append('storage')
from parse_support import NodeMessageParser
import Adafruit_BBIO.UART as UART
from datetime import datetime
from os.path import join,exists
from os import mkdir
from ConfigParser import SafeConfigParser
from storage import storage


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
parser = SafeConfigParser()
parser.read('node_config.ini')
serial_port = parser.get('base','port')
baud_rate = parser.get('base','baud')
log_dir = parser.get('base','logdir')
logfile = parser.get('base','logfile')
unrecognized = parser.get('base','unrecognized')

if not exists(log_dir):
    mkdir(log_dir)

store = storage()
nmp = NodeMessageParser()

UART.setup('UART1')

with open(join(log_dir,logfile),'a+',0) as event,\
     open(join(log_dir,unrecognized),'a+',0) as unrecognized:
    try:
        with serial.Serial(serial_port,baud_rate,timeout=2) as ser:
            log_event = lambda line: log(event,line)
            log_unrecognized = lambda line: log(unrecognized,line)

            log_event('Logging begins')

            # not sure about this (s,s,1). The documentation says no.
            # but nothing is being sent from the base station at the moment, so...
            ser.flushInput()
            s = io.TextIOWrapper(io.BufferedRWPair(ser,ser,1),newline=None)
            while True:
                try:
                    line = s.readline().strip()
                    if len(line) > 0:
                        d = nmp.parse_message(line)
                        node_id = d['node_id']
                        if node_id is not None:
                            #PRINT(str(node_id) + '\t' + line)
                            PRINT('from node {}: {}'.format(node_id,str(d)))
                            d['ReceptionTime'] = datetime.utcnow()
                            store.write(node_id,d)
                        else:
                            PRINT('whoa?')
                            log_unrecognized(line)
                except serial.SerialException:
                    PRINT('exploratory: USB-to-serial converters are EVIL')
                    log_event('USB-to-serial converters are EVIL')
                except Exception as e:
                    PRINT('huh?')
                    PRINT(e)
                    #raise e
    except KeyboardInterrupt:
        PRINT('exploratory: user interrupted')
        log_event('User interrupted')

    log_event('Logging terminated')

