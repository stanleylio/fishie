# Stanley H.I. Lio
import time, struct, io, fcntl, logging


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
        self.fw.write(b'\0')
        tmp = bytearray(b'\0')
        tmp.extend(self.fr.read(3))
        return struct.unpack('>I', tmp)[0]


if '__main__' == __name__:
    import argparse

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description='''Example: python3 tsys01.py --bus=1 --address=0x76''')
    parser.add_argument('--bus', metavar='bus', type=int, default=1, help='bus, one of {1, 2, ...}')
    parser.add_argument('--address', metavar='address', type=lambda x: int(x, base=16), default=0x77, help='I2C address')
    args = parser.parse_args()

    #print(s._read_prom())
    #print(s._raw_adc())
    #exit()
    while True:
        try:
            print(TSYS01(bus=args.bus, address=args.address).read())
        except IOError:
            logging.exception('Cant\'t reach sensor on bus {} channel {:x}'.format(args.bus, args.address))
        except KeyboardInterrupt:
            break
        time.sleep(0.1)
