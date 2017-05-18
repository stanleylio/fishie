# Class to handle communication with the ADAM4080 Frequency Counter
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# Ocean Technology Group
# SOEST, University of Hawaii
# All Rights Reserved, 2016
import serial,io,time,logging,traceback


class ADAM4080(object):
    def __init__(self,address,port,baud=9600):
        assert 2 == len(address)
        self._address = address
        self._s = serial.Serial(port,baud,timeout=1)
        self._sio = io.TextIOWrapper(io.BufferedRWPair(self._s,self._s,1),
                                     encoding='ascii',
                                     line_buffering=True,
                                     newline='\r')

    def __enter__(self):
        return self

    def __exit__(self,exc_type,exc_value,traceback):
        self._s.close()

    def __del__(self):
        self._s.close()

    def ReadAll(self):
        return [self.ReadFrequency(0),self.ReadFrequency(1)]

    def ReadFrequency(self,channel):
        try:
            if channel not in [0,1]:
                logging.debug('Channel must be either 0 or 1')
                return
            cmd = '#{}{}\r'.format(self._address,channel)
            r = self._query(channel,delimiter='#')
            r = r.strip()
            if r.startswith('>') and 9 == len(r.strip()):
                return int(r[1:],base=16)
        except:
            logging.debug(traceback.format_exc())
        return None
        
    def CheckModuleName(self):
        return '!{}4080'.format(self._address) == self.cmdReadModuleName().strip()

    def cmdReadModuleName(self):
        return self._query('M')

    def cmdReadFirmwareVersion(self):
        return self._query('F')

    def _query(self,cmd,delimiter='$'):
        self._s.flushInput()
        cmd = u'{}{}{}\r'.format(delimiter,self._address,cmd)
        #print cmd
        for i in range(2):
            self._sio.write(cmd)
            self._sio.flush()
            r = self._sio.readline()
            if len(r.strip()):
                return r
            logger.debug('_query(): nope')
        return ''


if '__main__' == __name__:
    #'DEBUG,INFO,WARNING,ERROR,CRITICAL'
    logging.basicConfig(level=logging.DEBUG)
    
    #import os
    with ADAM4080('04','/dev/ttyUSB2',9600) as fc:
        if fc.CheckModuleName():
            while True:
                #os.system('cls' if os.name == 'nt' else 'clear')
                print(fc.ReadFrequency(0),fc.ReadFrequency(1))
                time.sleep(0.1)
        else:
            print('CheckModuleName() returns False')

