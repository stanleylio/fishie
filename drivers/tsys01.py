# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2018
import time, struct, traceback, io, fcntl


class TSYS01:

    def __init__(self, address=0x77, bus=1):
        self.address = address
        self.fr = io.open('/dev/i2c-{}'.format(bus), 'rb', buffering=0)
        self.fw = io.open('/dev/i2c-{}'.format(bus), 'wb', buffering=0)
        I2C_SLAVE = 0x703
        fcntl.ioctl(self.fr, I2C_SLAVE, self.address)
        fcntl.ioctl(self.fw, I2C_SLAVE, self.address)

        self.reset()
        self._C = self._read_prom()

    def reset(self):
        self.fw.write(b'\x1E')
        time.sleep(0.003)

    def read(self):
        adc24 = self._raw_adc()
        adc16 = adc24/256
        # datasheet's example
        #k4,k3,k2,k1,k0 = 28446,24926,36016,32791,40781
        #adc16 = 36636
        k0, k1, k2, k3, k4 = self._C[0], self._C[1], self._C[2], self._C[3], self._C[4]
        t = -2*k4*1e-21*(adc16**4) + \
            4*k3*1e-16*(adc16**3) + \
            -2*k2*1e-11*(adc16**2) + \
            1*k1*1e-6*adc16 + \
            -1.5*k0*1e-2
        return round(t, 6)
        
    def _read_prom(self):
        C = []
        for i in range(5):
            self.fw.write(bytearray([0xAA - 2*i]))
            C.append(self.fr.read(2))
        return [struct.unpack('>H', c)[0] for c in C]

    def _raw_adc(self):
        self.fw.write(b'\x48')
        time.sleep(0.01)
        self.fw.write(bytearray([0]))
        tmp = bytearray(b'\0')
        tmp.extend(self.fr.read(3))
        return struct.unpack('>I', tmp)[0]


if '__main__' == __name__:
    s = TSYS01(bus=1)
    print(s._read_prom())
    #print(s._raw_adc())
    #exit()
    while True:
        try:
            print(s.read())
        except IOError:
            traceback.print_exc()
        except KeyboardInterrupt:
            break
        time.sleep(0.1)
    
