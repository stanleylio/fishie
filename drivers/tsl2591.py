# Stanley H.I. Lio
from time import sleep
from smbus import SMBus


class TSL2591(object):
    address = 0x29

    AGAIN = {0:1, 1:25, 2:428, 3:9876}
    ATIME = {0:100, 1:200, 2:300, 3:400, 4:500, 5:600}

    def __init__(self, bus=1, gain=1, integration_time=100):
        self.bus = SMBus(bus)
        #self._reset()
        self.gain(gain)
        self.integration_time(integration_time)
        self.enable()

    def check_ID(self):
        return 0x50 == self._read(0x12)

    def enable(self):
        self._write(0,0b11)

    def disable(self):
        self._write(0,0)

    def status(self):
        return self._read(0x13)

    def read(self):
        r = self.bus.read_i2c_block_data(self.address, 0x80 + 0x14, 4)
        mc = 65535
        if self._it == 0:
            mc = 37888
        r = {0:float((r[1] << 8) + r[0])/mc,
             1:float((r[3] << 8) + r[2])/mc}
        return r

    def integration_time(self,it=None):
        """Integration time should be one of {100,200,300,400,500,600}ms."""
        if it is not None:
            ii = {self.ATIME[k]:k for k in self.ATIME.keys()}
            if it not in ii:
                raise AttributeError('integration time must be one of {}'.\
                                     format(sorted(ii.keys())))
            # read-modify-write
            tmp = self._read(0x01)
            tmp = tmp & 0b11111000
            tmp = tmp | ii[it]
            self._write(0x01,tmp)

        # always return a fresh copy
        tmp = self._read(0x01)
        tmp = tmp & 0b00000111
        self._it = tmp
        return self.ATIME[tmp]

    def gain(self,gain=None):
        if gain is not None:
            ig = {self.AGAIN[k]:k for k in self.AGAIN.keys()}
            if gain not in ig:
                raise AttributeError('gain must be one of {}'.\
                                     format(sorted(ig.keys())))
            # read-modify-write
            tmp = self._read(0x01)
            tmp = tmp & 0b11001111
            tmp = tmp | ig[gain] << 4
            self._write(0x01, tmp)

        # always return a fresh copy
        tmp = self._read(0x01)
        tmp = (tmp & 0b00110000) >> 4
        return self.AGAIN[tmp]

    #def _reset(self):
    #    self._write(1,0x80)

    def _read(self, reg):
        # so this would be a so-called "combined protocol"
        return self.bus.read_byte_data(self.address,0x80 | reg)
        
    def _write(self, reg, value):
        self.bus.write_byte_data(self.address, 0x80 | reg, value)

    def __del__(self):
        #self.disable()
        pass

    #def duh(self):
    #    return self._read(0x11)


if '__main__' == __name__:
    s = TSL2591(bus=2)
    s.gain(1)
    s.integration_time(100)

    #print s.check_ID()
    #print s.duh()

    #s.gain(1)
    #print s.gain()
    #s.gain(25)
    #print s.gain()

    print('gain = {}x'.format(s.gain()))
    print('integration time = {:.1f}ms'.format(s.integration_time()))

    while True:
        r = s.read()
        print('ch0:{:.4f}, ch1:{:.4f}'.format(r[0], r[1]))
        sleep(0.1)

