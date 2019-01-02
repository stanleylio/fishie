# Class to handle communication with the ADAM4017 Data Acquisition Module (DAQ)
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# Ocean Technology Group
# University of Hawaii
# All Rights Reserved. 2018
import serial, io, time, logging


logger = logging.getLogger(__name__)


class ADAM4017(object):
    _bauds = {1200:'03', 2400:'04', 4800:'05', 9600:'06', 19200:'07', 38400:'08'}
    _ranges = {10:'08', 5:'09', 1:'0A', 500e-3:'0B', 150e-3:'0C'}
    
    def __init__(self, address, port, baud=9600):
        assert 2 == len(address)
        assert baud in self._bauds.keys()
        self._address = address
        self._s = serial.Serial(port, baud, timeout=1)
        self._sio = io.TextIOWrapper(io.BufferedRWPair(self._s, self._s, 1),
                                     encoding='ascii',
                                     line_buffering=True,
                                     newline='\r')
        self._currentinputrange = self.GetInputRange()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._s.close()

    def __del__(self):
        self._s.close()

    def _query(self, cmd, delimiter='$'):
        self._s.flushInput()
        cmd = u'{}{}{}\r'.format(delimiter, self._address, cmd)
        #print cmd
        for i in range(2):
            self._sio.write(cmd)
            self._sio.flush()
            r = self._sio.readline()
            if len(r.strip()):
                return r
            logger.debug('_query(): nope')
        return ''

    def CheckModuleName(self):
        return '!{}4017'.format(self._address) == self.cmdReadModuleName().strip()

    def SetInputRange(self, InputRange):
        logger.debug('SetInputRange(), from {} to {}'.format(self._currentinputrange, InputRange))
        assert InputRange in self._ranges.keys(),\
               'InputRange must be one of {}'.format(str(sorted(self._ranges.keys())))
        if not InputRange == self.GetInputRange():
            if self._configuration(InputRange=InputRange):
                self._currentinputrange = InputRange    # redundant coz GetInputRange() does the same
                logger.info('SetInputRange() changed to {}'.format(InputRange))
                return True
            else:
                logger.warning('_configuration(InputRange={}) failed'.format(InputRange))
                return False
        else:
            logger.debug('SetInputRange(): No change needed.')
            return True

    def SetInputRangeAuto(self,v):
        """Given a voltage v, set the DAQ to the best InputRange"""
        assert type(v) is float
        logger.debug('SetInputRangeAuto() for {}'.format(v))
        vs = sorted(self._ranges.keys())
        if v > max(vs):
            logger.error('SetInputRangeAuto(): the specified v={} is out of range'.format(v))
            return False
        for vr in vs:
            if vr >= v:
                r = self.SetInputRange(vr)
                if not r:
                    print('ayu')
                return r
        logger.warning('SetInputRangeAuto(): the supplied v is too large. Setting input range to maximum {}.'.format(max(vs)))
        return self.SetInputRange(max(vs))

    def GetInputRange(self):
        r = self.cmdConfigurationStatus()
        for k in self._ranges:
            if self._ranges[k] == r[3:5]:
                self._currentinputrange = k
                logger.debug('GetInputRange(): current = {}'.format(k))
                return k
        logger.warning('GetInputRange() failed: {}'.format(r))
        return None

    def ReadChannel(self,channel):
        logger.debug('ReadChannel()')
        r = self._query(cmd='{:01d}'.format(channel), delimiter='#')
        if r.startswith('>'):
            if self._currentinputrange < 1:
                return float(r[1:])/1e3
            return float(r[1:])

    def ReadAll(self):
        r = self._query(cmd='', delimiter='#')
        #print(r)
        if r.startswith('>'):
            r = r[1:]
            if 1+7*8 == len(r): # a '>' plus eight 7-chr fields
                try:
                    if self._currentinputrange < 1:
                        return [round(float(r[i*7:i*7+7])/1e3, 7) for i in range(8)]
                    else:
                        return [round(float(r[i*7:i*7+7]), 7) for i in range(8)]
                except ValueError:
                    logger.error('wut? {}'.format(str(r)))
        return None

    def _configuration(self, NewAddress=None, InputRange=None, NewBaud=None, FCI=None):
        """This call is costly - takes 7 sec for self-cal after configuration change. P.118
FCI: Format, Checksum and Integration time. P.117"""
        if NewBaud is not None or FCI is not None:
            print('need to do something with the INIT* pin... check the manual.')
            #raise NotImplementedError
        r = self.cmdConfigurationStatus()
        if 10 == len(r) and '!' == r[0] and '\r' == r[-1] and self._address == r[1:3]:
            AA = self._address
            NN = NewAddress if NewAddress is not None else self._address
            TT = self._ranges[InputRange] if InputRange is not None else r[3:5]
            CC = self._bauds[NewBaud] if NewBaud is not None else r[5:7]
            FF = FCI if FCI is not None else r[7:9]
            cmd = u'%' + AA + NN + TT + CC + FF
            self._sio.write(cmd + '\r')
            self._sio.flush()
            r = self._sio.readline()
            if r.startswith('!') and self._address == r[1:3]:
                logger.info('Wait seven seconds for self-calibration...')
                # The DAQ may respond immediately, but the new settings may not
                # come into effect at the same time. There is no indication when
                # the new settings become effective, so the 7-second wait is mandatory.
                # This makes ReadChannelAutoRange() impractical.
                time.sleep(7)
                return True
            logger.warning('_configuration(): {}'.format(r))
            return False
        elif 4 == len(r) and '?' == r[0] and '\r' == r[-1] and self._address == r[1:3]:
            logger.warning('Invalid command. Response={}'.format(r))    # P.121
        else:
            logger.debug('Unexpected response from serial bus: {}'.format(r))
        return False
        
    def cmdConfigurationStatus(self):
        return self._query('2')

    def cmdReadModuleName(self):
        return self._query('M')

    def cmdReadFirmwareVersion(self):
        return self._query('F')


if '__main__' == __name__:
    logging.basicConfig()
    #'DEBUG,INFO,WARNING,ERROR,CRITICAL'
    logger.setLevel(logging.DEBUG)
    
    import os
    with ADAM4017('07', '/dev/ttyUSB0', 9600) as daq:
        #print(daq.cmdConfigurationStatus())
        #print(daq.cmdReadModuleName())
        #print(daq.cmdReadFirmwareVersion())

        if daq.CheckModuleName():
            if daq.SetInputRange(5):
                print(daq.ReadAll())
                while True:
                    #os.system('cls' if os.name == 'nt' else 'clear')
                    #print(daq.ReadChannel(2))
                    print(daq.ReadAll())
                    time.sleep(0.1)
        else:
            print('CheckModuleName() returns False')

