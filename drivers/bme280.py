# Driver for talking to the BME280 pressure temperature humidity sensor.
# Fixed OSR=16.
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2018
import time, struct, io, fcntl, logging


logger = logging.getLogger(__name__)


class BME280:
    def __init__(self, address=0x77, bus=1, **kwargs):
        self.address = address
        self.fr = io.open('/dev/i2c-{}'.format(bus), 'rb', buffering=0)
        self.fw = io.open('/dev/i2c-{}'.format(bus), 'wb', buffering=0)
        I2C_SLAVE = 0x703
        fcntl.ioctl(self.fr, I2C_SLAVE, self.address)
        fcntl.ioctl(self.fw, I2C_SLAVE, self.address)

        self.reset()
        time.sleep(0.1)
        #self.check_ID()
        #self._read_prom()
        
        osrs_h = 0b101
        self.fw.write(bytearray([0xF2, osrs_h]))

        osrs_t = 0b101
        osrs_p = 0b101
        mode = 0b11
        self.fw.write(bytearray([0xF4, (osrs_t << 5) + (osrs_p << 2) + mode]))


    def check_ID(self):
        self.fw.write(b'\xD0')
        return 0x60 == ord(self.fr.read(1))

    def reset(self):
        self.fw.write(b'\xE0\xB6')
        
    def _read_prom(self):
        self.fw.write(b'\x88')
        self.dig_T1 = struct.unpack('<H', self.fr.read(2))[0]
        self.fw.write(b'\x8A')
        self.dig_T2 = struct.unpack('<h', self.fr.read(2))[0]
        self.fw.write(b'\x8C')
        self.dig_T3 = struct.unpack('<h', self.fr.read(2))[0]
        self.fw.write(b'\x8E')
        
        self.dig_P1 = struct.unpack('<H', self.fr.read(2))[0]
        self.fw.write(b'\x90')
        self.dig_P2 = struct.unpack('<h', self.fr.read(2))[0]
        self.fw.write(b'\x92')
        self.dig_P3 = struct.unpack('<h', self.fr.read(2))[0]
        self.fw.write(b'\x94')
        self.dig_P4 = struct.unpack('<h', self.fr.read(2))[0]
        self.fw.write(b'\x96')
        self.dig_P5 = struct.unpack('<h', self.fr.read(2))[0]
        self.fw.write(b'\x98')
        self.dig_P6 = struct.unpack('<h', self.fr.read(2))[0]
        self.fw.write(b'\x9A')
        self.dig_P7 = struct.unpack('<h', self.fr.read(2))[0]
        self.fw.write(b'\x9C')
        self.dig_P8 = struct.unpack('<h', self.fr.read(2))[0]
        self.fw.write(b'\x9E')
        self.dig_P9 = struct.unpack('<h', self.fr.read(2))[0]
        self.fw.write(b'\xA1')
        
        self.dig_H1 = struct.unpack('<B', self.fr.read(1))[0]
        self.fw.write(b'\xE1')
        self.dig_H2 = struct.unpack('<h', self.fr.read(2))[0]
        self.fw.write(b'\xE3')
        self.dig_H3 = struct.unpack('<B', self.fr.read(1))[0]

        self.fw.write(b'\xE4')
        e4, e5, e6 = self.fr.read(3)
        self.dig_H4 = (e4 << 4) | (e5 & 0b1111)
        self.dig_H5 = ((e5 >> 4) & 0b11110000) | (e6 << 4)
        self.fw.write(b'\xE7')
        self.dig_H6 = struct.unpack('<b', self.fr.read(1))[0]

        '''print('dig_T1 = {}'.format (self.dig_T1))
        print('dig_T2 = {}'.format (self.dig_T2))
        print('dig_T3 = {}'.format (self.dig_T3))
        
        print('dig_P1 = {}'.format (self.dig_P1))
        print('dig_P2 = {}'.format (self.dig_P2))
        print('dig_P3 = {}'.format (self.dig_P3))
        print('dig_P4 = {}'.format (self.dig_P4))
        print('dig_P5 = {}'.format (self.dig_P5))
        print('dig_P6 = {}'.format (self.dig_P6))
        print('dig_P7 = {}'.format (self.dig_P7))
        print('dig_P8 = {}'.format (self.dig_P8))
        print('dig_P9 = {}'.format (self.dig_P9))

        print('dig_H1 = {}'.format (self.dig_H1))
        print('dig_H2 = {}'.format (self.dig_H2))
        print('dig_H3 = {}'.format (self.dig_H3))
        print('dig_H4 = {}'.format (self.dig_H4))
        print('dig_H5 = {}'.format (self.dig_H5))
        print('dig_H6 = {}'.format (self.dig_H6))'''

    def read(self):
        self._read_prom()
        adc_T, adc_P, adc_H = self.read_adc()

        # T
        var1 = (adc_T/16384 - self.dig_T1/1024) * self.dig_T2
        var2 = (adc_T/131072 - self.dig_T1/8192)*(adc_T/131072 - self.dig_T1/8192)*self.dig_T3
        t_fine = var1 + var2
        T = round(t_fine/5120, 3)

        # P
        var1 = t_fine/2 - 64000
        var2 = var1*var1*self.dig_P6/32768
        var2 = var2 + var1*self.dig_P5*2
        var2 = var2/4 + self.dig_P4*65536
        var1 = (self.dig_P3*var1*var1/524288 + self.dig_P2*var1)/524288
        var1 = (1 + var1/32768)*self.dig_P1
        if 0 == var1:
            P = 0
        else:
            p = 1048576 - adc_P
            p = (p - (var2/4096))*6250/var1
            var1 = self.dig_P9*p*p/2147483648
            var2 = p*self.dig_P8/32768
            P = p + (var1 + var2 + self.dig_P7)/16
            P = round(P/1000, 3)  # kPa

        # RH
        var_H = t_fine - 76800
        var_H = (adc_H - (self.dig_H4*64 + self.dig_H5/16384*var_H))*\
                (self.dig_H2/65536*(1 + self.dig_H6/67108864*var_H*\
                                      (1 + self.dig_H3/67108864*var_H)))
        var_H = var_H*(1 - self.dig_H1*var_H/524288)
        var_H = round(max(0, min(var_H, 100)), 2)
        
        return {'t':T, 'p':P, 'rh':var_H}
    
    def read_adc(self):
        delay_ms = (1.23 + 2.3*16 + 2.3*16 + 0.575 + 2.3*16 + 0.575)/1000
        self.fw.write(b'\xFA')
        time.sleep(delay_ms)
        msb, lsb, xlsb = self.fr.read(3)
        #print(msb, lsb, xlsb)
        xlsb = (xlsb >> 4) & 0b1111
        t_adc = (msb << 12) | (lsb << 4) | xlsb

        self.fw.write(b'\xF7')
        time.sleep(delay_ms)
        msb, lsb, xlsb = self.fr.read(3)
        xlsb = (xlsb >> 4) & 0b1111
        p_adc = (msb << 12) | (lsb << 4) | xlsb

        self.fw.write(b'\xFD')
        time.sleep(delay_ms)
        msb, lsb = self.fr.read(2)
        rh_adc = (msb << 8) + lsb

        return t_adc, p_adc, rh_adc


if '__main__' == __name__:

    import argparse

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description='''Example: python3 bme280.py --bus=1 --address=0x76''')
    parser.add_argument('--bus', metavar='bus', type=int, default=1, help='bus, one of {1, 2, ...}')
    parser.add_argument('--address', metavar='address', type=lambda x: int(x, base=16), default=0x76, help='I2C address')
    args = parser.parse_args()

    while True:
        try:
            bme = BME280(bus=args.bus, address=args.address)
            print(bme.read())
        except KeyboardInterrupt:
            break
        except:
            logging.exception('wut?')
