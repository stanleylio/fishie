from __future__ import division
import time,struct,traceback
from smbus import SMBus


class TSYS01(object):

    def __init__(self,address=0x77,bus=1):
        self.bus = SMBus(bus)
        self.address = address

        self.reset()
        self._C = self._read_prom()

    def reset(self):
        self.bus.write_byte(self.address,0x1E)
        time.sleep(0.05)

    def read(self):
        adc24 = self._raw_adc()
        adc16 = adc24/256
        k4 = self._C[1]
        k3 = self._C[2]
        k2 = self._C[3]
        k1 = self._C[4]
        k0 = self._C[5]
        # datasheet's example
        #k4,k3,k2,k1,k0 = 28446,24926,36016,32791,40781
        #adc16 = 36636
        return -2*k4*1e-21*adc16**4 + \
               4*k3*1e-16*adc16**3 + \
               -2*k2*1e-11*adc16**2 + \
               1*k1*1e-6*adc16 + \
               -1.5*k0*1e-2
        
    def _read_prom(self):
        tmp = [self.bus.read_byte_data(self.address,i) for i in range(0xA0,0xAE+1)]
        C = struct.unpack('>HHHHHHHB',''.join([chr(c) for c in tmp]))
        return C

    def _raw_adc(self):
        self.bus.write_byte(self.address,0x48)
        time.sleep(0.01)
        tmp = self.bus.read_i2c_block_data(self.address,0,3)
        tmp.insert(0,0)
        return struct.unpack('>I',''.join([chr(c) for c in tmp]))[0]


if '__main__' == __name__:
    s = TSYS01()
    #print(s._read_prom())
    #print(s._raw_adc())
    while True:
        try:
            print(s.read())
        except IOError:
            traceback.print_exc()
        time.sleep(0.2)
    
