import time

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

class EZO:
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

    def _r(self,cmd,wait=1):
        # don't need the patch after all. tho the EZO series is sure non-standard...
        #i2c.writeRaw8(ord('I'))
        if 1 == len(cmd):
            self.i2c.write8(ord(cmd),0)         # so abitrary...
        elif len(cmd) > 1:
            tmp = [ord(c) for c in cmd]
            self.i2c.writeList(tmp[0],tmp[1:])  # awkward...
        else:
            PRINT('EZO_pH: HUH?')
        time.sleep(wait)
        tmp = self.i2c.readList(self.address,self.MAX_LEN)
        
        if self.lowpower:
            self.sleep()
        
        if self.Success == tmp[0]:
            return ''.join([chr(c) for c in tmp[1:] if 0 != c])
        elif self.Failed == tmp[0]:
            PRINT('EZO_pH: read failed')
            PRINT(tmp)
            return None
        elif self.Pending == tmp[0]:
            PRINT('EZO_pH: Pending')
            return None
        elif self.NoData == tmp[0]:
            PRINT('EZO_pH: NoData')
            return None
        else:
            PRINT('EZO_pH: error ({})'.format(tmp[0]))
            PRINT(tmp)
            return None

