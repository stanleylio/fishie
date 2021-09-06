import time, struct, io, fcntl


class TSYS01:

    def __init__(self, *, address=0x77, bus=1, validate_checksum=False):
        self.address = address
        self.fr = io.open('/dev/i2c-{}'.format(bus), 'rb', buffering=0)
        self.fw = io.open('/dev/i2c-{}'.format(bus), 'wb', buffering=0)
        I2C_SLAVE = 0x703
        fcntl.ioctl(self.fr, I2C_SLAVE, self.address)
        fcntl.ioctl(self.fw, I2C_SLAVE, self.address)

        self.reset()
        self._prom = self._read_prom()
        # extract the calibration factors
        self._CF = struct.unpack('>HHHHHHH', self._prom)[:-2][::-1]
        # and the serial number
        tmp = struct.unpack('>HH', self._prom[-4:])
        self.SN = (2**8)*tmp[0] + (tmp[1] >> 8)
        
        if validate_checksum and (0 != sum(self._prom) % 0x100):
            raise RuntimeError(f"Invalid checksum. PROM={self._prom}")

    def reset(self):
        self.fw.write(b'\x1E')
        time.sleep(0.003)

    def read(self):
        adc24 = self._raw_adc()
        adc16 = adc24/256
        # datasheet's example
        #k4,k3,k2,k1,k0 = 28446,24926,36016,32791,40781
        #adc16 = 36636
        k0, k1, k2, k3, k4 = self._CF[0:5]
        t = -2*k4*1e-21*(adc16**4) + \
            4*k3*1e-16*(adc16**3) + \
            -2*k2*1e-11*(adc16**2) + \
            1*k1*1e-6*adc16 + \
            -1.5*k0*1e-2
        return round(t, 9)
        
    def _read_prom(self):
        # 5 uint16_t, plus a 24-bit serial number, then a 8-bit checksum
        # Checksum: assert 0 == sum(r) % 0x100
        # Reading from 0xA2 up, you get k4 to k0, then SN23..8, and SN7..0 | checksum.
        C = bytearray()
        # it doesn't auto-increment the pointer, so you can't read more
        # than 2-byte each call.
        for addr in range(0xA2, 0xAE + 2, 2):
            self.fw.write(bytearray([addr]))
            C += self.fr.read(2)
        return bytes(C)

    def _raw_adc(self):
        self.fw.write(b'\x48')
        time.sleep(0.01)
        self.fw.write(b'\0')
        tmp = bytearray(b'\0')
        tmp.extend(self.fr.read(3))
        return struct.unpack('>I', tmp)[0]


if '__main__' == __name__:
    import argparse, sys, logging

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description='''Example: python3 tsys01.py --bus=1 --address=0x76''')
    parser.add_argument('--bus', metavar='bus', type=int, default=1, help='bus, one of {1, 2, ...}')
    parser.add_argument('--address', metavar='address', type=lambda x: int(x, base=16), default=0x77, help='I2C address')
    args = parser.parse_args()

    #sensor = TSYS01()
    # In terms of serial number, you could use the Serial Number field:
    #print(hex(sensor.SN))
    # ... or you could just use the whole PROM, since the calibration
    # factors are not expected to change and are likely to be unique
    # (yay free entropy):
    #print(''.join([f"{b:02x}" for b in sensor._prom]))

    while True:
        try:
            print(TSYS01(bus=args.bus, address=args.address).read())
        except IOError:
            logging.exception('Can\'t reach sensor on bus {} channel {:x}'.format(args.bus, args.address))
        except KeyboardInterrupt:
            break
        time.sleep(0.1)
