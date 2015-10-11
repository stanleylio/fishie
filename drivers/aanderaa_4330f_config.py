#!/usr/bin/python
import serial,time

#'do stop'
#'get all'
#'set interval(600)'
#'save'
#'do sample'
#'do start'

with serial.Serial('COM12',9600,timeout=3) as s:
    s.flushOutput()
    s.flushInput()
    
    response = '*'
    while not response.startswith('#'):
        if len(response) == 0 or response.startswith('*'):
            print '[do stop]'
            s.write('do stop\r\n')
        response = s.readline().strip()
        print response

    
    response = '*'
    while not response.startswith('#'):
        if len(response) == 0 or response.startswith('*'):
            print '[get all]'
            s.write('get all\r\n')
        response = s.readline().strip()
        print response

print 'terminated.'

