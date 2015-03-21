#!/usr/bin/python
# get lines of text from serial port, save them to a file
# code found on web, written by jbeale
# http://www.raspberrypi.org/forums/viewtopic.php?f=44&t=64545

from __future__ import print_function
import serial, io

addr  = '/dev/ttyO4'  # serial port to read data from
ser_out = serial.Serial(port = "/dev/ttyUSB0", baudrate=9600)
baud  = 9600            # baud rate for serial port
fname = '/root/optodeData/optodeData.dat'   # log file to save data in
fmode = 'a'             # log file mode = append

with serial.Serial(addr,9600) as pt, open(fname,fmode) as outf:
    spb = io.TextIOWrapper(io.BufferedRWPair(pt,pt,1),
        encoding='ascii', errors='ignore', newline='\r',line_buffering=True)
    spb.readline()  # throw away first line; likely to start mid-sentence (incomplete)
    while (1):
        x = spb.readline()  # read one line of text from serial port
        print (x,end='')    # echo line of text on-screen
        ser_out.write(x)  # echo line of text to USB serial XBee
        outf.write(x)       # write line of text to file
        outf.flush()        # make sure it actually gets written out
