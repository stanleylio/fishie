"""Stanley Lio, hlio@usc.edu
All Rights Reserved. February 2015
"""
from smbus import SMBus
from time import sleep


def PRINT(s):
    #pass
    print(s)

class EZO(object):

    MAX_LEN = 32

    NoData = 255
    Pending = 254
    Failed = 2
    Success = 1

    def __init__(self,address,bus=1,lowpower=False):
        self.bus = SMBus(bus)
        self.address = address
        self.lowpower = lowpower

    def __enter__(self):
        return self

    # programmer's note
    # http://stackoverflow.com/questions/3394835/args-and-kwargs
    #def __exit__(self,type,value,tb):
    def __exit__(self,*ignored):
        self.sleep()
        return True

    def device_information(self):
        return self._r('I',0.3)

    # the supply voltage field might be useful
    def status(self):
        return self._r('STATUS',0.3)

    # supply voltage at the sensor
    def supply_v(self):
        return float(self.status().strip().split(',')[-1])

    def sleep(self):
        cmd = 'SLEEP'
        tmp = [ord(c) for c in cmd]
        self.bus.write_i2c_block_data(self.address,tmp[0],tmp[1:])

    # set or read the compensation paramter T temperature
    # NOTE: this value is for sensor calibration. it's NOT obtained from the sensor
    # almost the same as k(), except for the boundary check and debug messages
    # factoring this function makes code maintenance easier, but I lose the ability
    # to do custom debug print
    def t(self,new=None,from_=''):
        tmp = self._r('T,?',0.3)    # always do a read first
        if tmp.startswith('?T,'):
            current = float(tmp[3:6])
            if new is None:
                if self.lowpower:
                    self.sleep()
                return current
            elif current != new:
                # in Celsius.
                # NOAA says -2 is the lower limit, but said nothing about the upper limit
                # but it's not my job to judge so proceed anyway
                if new >= 50 or new <= -10:
                    PRINT(from_ + 'warning: strange... are you sure about the new temperature?')

                # sensor stores only integer T
                # better be explicit
                PRINT(from_ + 'update current T = {:.1f} to new T = {:.1f}'.format(current,new))
                
                # inconsistent... sensor accepts only integer but the spec says float.
                #cmd = 'T,{:.1f}'.format(new)
                cmd = 'T,{:.1f}'.format(round(new))
                self._r(cmd,0.3)    # ignore the response
            else:
                PRINT(from_ + 'supplied T == current T = {:.0f} Deg.C, no update required'.format(current))
        else:
            PRINT(from_ + 'cannot retrieve T value from sensor')
        if self.lowpower:
            self.sleep()

    def _r(self,cmd,wait=1):
        tmp = len(cmd)
        assert tmp > 0
        if 1 == tmp:
            self.bus.write_byte_data(ord(cmd),0)    # so arbitrary...
        else:
            tmp = [ord(c) for c in cmd]
            self.bus.write_i2c_block_data(self.address,tmp[0],tmp[1:])  # awkward...
        
        sleep(wait)
        # WTH... TODO scope this
        tmp = self.bus.read_i2c_block_data(self.address,self.address,self.MAX_LEN)
        
        if self.lowpower:
            self.sleep()

#        print ''.join([chr(c) for c in tmp[1:] if 0 != c])
        
        if self.Success == tmp[0]:
            return ''.join([chr(c) for c in tmp[1:] if 0 != c])
        elif self.Failed == tmp[0]:
            PRINT('EZO::_r(): read failed')
            PRINT(tmp)
            return None
        elif self.Pending == tmp[0]:
            PRINT('EZO::_r(): Pending')
            return None
        elif self.NoData == tmp[0]:
            PRINT('EZO::_r(): NoData')
            return None
        else:
            PRINT('EZO::_r(): error ({})'.format(tmp[0]))
            PRINT(tmp)
            return None

