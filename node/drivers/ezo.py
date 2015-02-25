import time

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

def PRINT(s):
    #pass
    print(s)

class EZO(object):
    NoData = 255
    Pending = 254
    Failed = 2
    Success = 1

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
        self.i2c.writeList(tmp[0],tmp[1:])

    # set or read the compensation paramter T temperature
    # NOTE: this value is for sensor calibration. it's NOT obtained from the sensor
    # almost the same as k(), except for the boundary check and debug messages
    # factoring this function makes code maintenance easier, but I lose the ability
    # to do custom debug print
    def t(self,new=None):
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
                    PRINT('warning: strange... are you sure about the new temperature?')

                # sensor stores only integer T
                # better be explicit
                PRINT('update current T = {:.0f} to new T = {:.0f}'.format(current,new))
                
                # inconsistent... sensor accepts only integer but the spec says float.
                #cmd = 'T,{:.1f}'.format(new)
                cmd = 'T,{:.0f}'.format(new)
                self._r(cmd,0.3)    # ignore the response
            else:
                PRINT('supplied T == current T = {:.0f} Deg.C, no update required'.format(current))
        else:
            PRINT('cannot retrieve T value from sensor')
        if self.lowpower:
            self.sleep()

    def _r(self,cmd,wait=1):
        # don't need the patch after all. tho the EZO series is sure non-standard...
        #i2c.writeRaw8(ord('I'))
        if 1 == len(cmd):
            self.i2c.write8(ord(cmd),0)         # so abitrary...
        elif len(cmd) > 1:
            tmp = [ord(c) for c in cmd]
            self.i2c.writeList(tmp[0],tmp[1:])  # awkward...
        else:
            PRINT('EZO: HUH?')
        time.sleep(wait)
        tmp = self.i2c.readList(self.address,self.MAX_LEN)
        
        if self.lowpower:
            self.sleep()
        
        if self.Success == tmp[0]:
            return ''.join([chr(c) for c in tmp[1:] if 0 != c])
        elif self.Failed == tmp[0]:
            PRINT('EZO: read failed')
            PRINT(tmp)
            return None
        elif self.Pending == tmp[0]:
            PRINT('EZO: Pending')
            return None
        elif self.NoData == tmp[0]:
            PRINT('EZO: NoData')
            return None
        else:
            PRINT('EZO: error ({})'.format(tmp[0]))
            PRINT(tmp)
            return None

