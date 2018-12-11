# Stanley H.I. Lio
from time import sleep
from smbus import SMBus


class TCS34725(object):
    address = 0x29

    AGAIN = {0:1, 1:4, 2:16, 3:60}

    # The middle one should be 0xd6 for the table to be correct...
    # unless, of course, the other two were wrong and 0xD5 is in fact
    # correct.
    # in ms.
    ATIME = {0xff:2.4, 0xf6:24, 0xd6:101, 0xc0:154, 0x00:700}
    
    def __init__(self, bus=1, gain=1, integration_time=2.4):
        self.bus = SMBus(bus)
        self.gain(gain)
        # must be called at least once as readCRGB() relies on its cached value
        self.integration_time(integration_time)
        self.enable()

    def check_ID(self):
        return 0x44 == self._read(0x12)

    def enable(self):
        """see notes on P.15"""
        self._write(0,0b1)
        sleep(0.003)
        self._write(0, 0b11)

    def disable(self):
        self._write(0, 0)
        
    def status(self):
        return self._read(0x13)

    def read(self):
        r = self.bus.read_i2c_block_data(self.address, 0x80 + 0x14, 8)
        mc = min((256 - self._it)*1024, 65535)
        r = {'c':float((r[1] << 8) + r[0])/mc,
             'r':float((r[3] << 8) + r[2])/mc,
             'g':float((r[5] << 8) + r[4])/mc,
             'b':float((r[7] << 8) + r[6])/mc,}
        return r

    def integration_time(self, it=None):
        """Integration time it should be one of {2.4,24,101,154,700}ms."""
        if it is not None:
            ii = {self.ATIME[k]:k for k in self.ATIME.keys()}
            if it not in ii:
                raise AttributeError('integration time must be one of {}'.\
                                     format(sorted(ii.keys())))
            self._write(0x01, ii[it])
        tmp = self._read(0x01)
        self._it = tmp
        return self.ATIME[tmp]

    def gain(self,gain=None):
        """gain should be one of {1,4,16,60}."""
        if gain is not None:
            ig = {self.AGAIN[k]:k for k in self.AGAIN.keys()}
            if gain not in ig:
                raise AttributeError('gain must be one of {})'.\
                                     format(sorted(ig.keys())))
            self._write(0x0f, ig[gain])
        return self.AGAIN[self._read(0x0f) & 0b11]
    
    #def duh(self):
    #    print [self._read(0x00),self._read(0x01),self._read(0x0f)]

    def _read(self,reg):
        # so this would be a so-called "combined protocol"
        return self.bus.read_byte_data(self.address, 0x80 + reg)
        
    def _write(self,reg,value):
        self.bus.write_byte_data(self.address, 0x80 + reg, value)

    def __del__(self):
        #self.disable()
        pass


if '__main__' == __name__:
    import traceback
    
    s = TCS34725(bus=1)
    s.gain(1)                   # {1x,4x,16x,60x}
    s.integration_time(2.4)     # {2.4ms,24ms,101ms,154ms,700ms}

    #s.duh()
    #print s.gain()
    #print s.integration_time()

    while True:
        try:
            r = s.read()
            #print ''.join(['c']*int(round(r['c']*10))) + ' ' + '{:.3f}'.format(r['c'])
            #print 'r{:.2f}, g{:.2f}, b{:.2f}'.format(r['r'],r['g'],r['b'])

            a = [int(round(r[tmp]*10)) for tmp in ['r', 'g', 'b']]
            a = [tmp[1]*tmp[0] + ' '*(10 - tmp[0]) for tmp in zip(a,['r', 'g', 'b'])]
            print '{}\t{}\t{}'.format(a[0], a[1], a[2])
            sleep(0.1)
        except IOError:
            traceback.print_exc()
            pass
