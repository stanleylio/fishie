#!/usr/bin/python3
# Driver for the MS5803-14BA pressure sensor
# Tested working on Beaglebone Black (rev.C 4GB) and Raspberry Pi A+ (256MB)

# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2018
import time, struct, io, fcntl, logging


logger = logging.getLogger(__name__)


class MS5803_14BA:

    osr = {256:0, 512:2, 1024:4, 2048:6, 4096:8}
    conv_time = {256:0.0006, 512:0.00117, 1024:0.00228, 2048:0.00454, 4096:0.00904}

    def __init__(self, address=0x76, bus=1):
        self.address = address
        self.fr = io.open('/dev/i2c-{}'.format(bus), 'rb', buffering=0)
        self.fw = io.open('/dev/i2c-{}'.format(bus), 'wb', buffering=0)
        I2C_SLAVE = 0x703   # but why?
        fcntl.ioctl(self.fr, I2C_SLAVE, self.address)
        fcntl.ioctl(self.fw, I2C_SLAVE, self.address)

        self.reset()

    def __enter__(self):
        return self

    def __exit__(self, *ignored):
        return True

    def reset(self):
        self.fw.write(b'\x1E')
        time.sleep(0.05)

    # {'p':kPa, 't':Deg.C}
    # OverSampling Rate (osr)
    # osr can be one of {256,512,1024,2048,4096}
    def read(self, osr=4096):

        assert osr in self.osr
        
        C = self._read_prom()
        D1 = self._raw_pressure(osr=osr)
        D2 = self._raw_temperature(osr=osr)
        dT = D2 - C[5]*(2**8)
        TEMP = 2000 + dT*C[6]/(2**23)
        OFF = C[2]*(2**16) + (C[4]*dT)/(2**7)
        SENS = C[1]*(2**15) + (C[3]*dT)/(2**8)

        # - - -
        # "SECOND ORDER TEMPERATURE COMPENSATION" (P.9)
        if TEMP < 2000:
            T2 = 3*(dT**2)/2**33
            OFF2 = 3*((TEMP - 2000)**2)/2
            SENS2 = 5*((TEMP - 2000)**2)/(2**3) # 2**3 == readability...

            if TEMP < -1500:
                OFF2 = OFF2 + 7*((TEMP + 1500)**2)
                SENS2 = SENS2 + 4*((TEMP + 1500)**2)
        else:
            T2 = 7*(dT**2)/2**37
            OFF2 = ((TEMP-2000)**2)/(2**4)
            SENS2 = 0

        TEMP = TEMP - T2
        OFF = OFF - OFF2
        SENS = SENS - SENS2
        # - - -

        P = (D1*SENS/(2**21) - OFF)/(2**15)

        TEMP = round(TEMP/100., 3)
        P = round(P/100., 3)
        return {'p':P, 't':TEMP}

    def pretty(self, r=None, *args, **kwargs):
        if r is None:
            r = self.read(*args, **kwargs)
        return '{} kPa, {} Deg.C'.format(r['p'], r['t'])


    '''# STRANGE. AVR reads (slightly) differently. And the scope agrees with it.
    # read factory calibration parameters, C[6]
    def _read_prom(self):
        tmp = [self.bus.read_byte_data(self.address,i) for i in range(0xA0,0xAE+1)]
        C = struct.unpack('>HHHHHHHB',''.join([chr(c) for c in tmp]))
        return C'''

    # This is adapted from the driver for TSYS01. That sensor works correctly
    # with this, and the readout of this one agrees with that from the Arduino.
    # So this should be the correct version, but I have no idea why the old
    # one doesn't work. Strange that the difference is very small - digital
    # stuff usually either works perfectly or doesn't work at all.
    def _read_prom(self):
        C = []
        for i in range(7):
            self.fw.write(bytes([0xA0 + 2*i]))
            C.append(self.fr.read(2))
        return [struct.unpack('>H',c)[0] for c in C]

    # uncompensated pressure, D1
    def _raw_pressure(self, osr=4096):
        self.fw.write(bytes([0x40 + self.osr[osr]]))
        time.sleep(0.02)
        self.fw.write(b'\0')
        tmp = bytearray(b'\0')
        tmp.extend(self.fr.read(3))
        return struct.unpack('>I', tmp)[0]

    # temperature, D2
    def _raw_temperature(self, osr=4096):
        self.fw.write(bytes([0x50 + self.osr[osr]]))
        time.sleep(0.02)
        self.fw.write(bytes([0]))
        tmp = bytearray(b'\0')
        tmp.extend(self.fr.read(3))
        return struct.unpack('>I', tmp)[0]


if '__main__' == __name__:

    logger.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)

    bus = 1
    print('using bus {}'.format(bus))
    ms = MS5803_14BA(bus=bus, address=0x76)
    
    #print('raw pressure: {}'.format(ms._raw_pressure()))
    #print('raw_temperature: {}'.format(ms._raw_temperature()))

    while True:
        #print('\x1b[2J\x1b[;H')
        print(ms.pretty())
        time.sleep(0.1)

