#!/usr/bin/python

# Serial capture

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

import serial

print 'no you don\'t want to run this. (comment me out if you do)'
exit()

#serial_name = 'COM18'
serial_name = '/dev/ttyO1'
baud = 9600

raw_file_name = 'serial_cap.txt'

try:
    with serial.Serial(serial_name,baud,timeout=1) as s,open(raw_file_name,'w',0) as raw:
        while True:
            line = s.readline().rstrip()
            if len(line) > 0:
                print line
                raw.write(line + '\n')
                raw.flush()
                #s.write(line)
except KeyboardInterrupt:
    print 'user interrupted'

print 'closed'

