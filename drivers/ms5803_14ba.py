from __future__ import division
import smbus,time,struct

# Driver for the MS5803-14BA pressure sensor
# Tested working on Beaglebone Black (rev.B, 2GB) and Raspberry Pi A+ (256MB)

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

class MS5803_14BA:

    osr = {256:0,512:2,1024:4,2048:6,4096:8}

    def __init__(self,address=0x76,bus=1):
        self.bus = smbus.SMBus(bus)
        self.address = address

        self.reset()
        self._C = self._read_prom()

    def __enter__(self):
        return self

    def __exit__(self,*ignored):
        return True

    def reset(self):
        self.bus.write_byte(self.address,0x1E)
        time.sleep(0.05)

    # {'p':kPa, 't':Deg.C}
    # OverSampling Rate (osr)
    # osr can be one of {256,512,1024,2048,4096}
    def read(self,osr=4096):
        D1 = self._raw_pressure(osr=osr)
        D2 = self._raw_temperature(osr=osr)
        C = self._C
        dT = D2 - C[5]*(2**8)
        TEMP = 2000L + dT*C[6]/(2**23)
        OFF = long(C[2])*(2**16) + (long(C[4])*dT)/(2**7)
        SENS = long(C[1])*(2**15) + (long(C[3])*dT)/(2**8)

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

        P = (long(D1)*SENS/(2**21) - OFF)/(2**15)

        TEMP = round(TEMP/100.,3)
        P = round(P/100.,3)
        return {'p':P,'t':TEMP}

    def pretty(self,r=None):
        if r is None:
            r = self.read()
        return '{} kPa, {} Deg.C'.format(r['p'],r['t'])


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
        C = [self.bus.read_word_data(self.address,0xA0 + 2*i) for i in range(7)]
        C = [struct.unpack('<H',struct.pack('>H',c))[0] for c in C]
        return C

    # uncompensated pressure, D1
    def _raw_pressure(self,osr=4096):
        self.bus.write_byte(self.address,0x40 + self.osr[osr])
        time.sleep(0.01)
        tmp = self.bus.read_i2c_block_data(self.address,0,3)
        tmp.insert(0,0)
        D1 = struct.unpack('>I',''.join([chr(c) for c in tmp]))[0]
        return D1

    # temperature, D2
    def _raw_temperature(self,osr=4096):
        self.bus.write_byte(self.address,0x50 + self.osr[osr])
        time.sleep(0.01)
        tmp = self.bus.read_i2c_block_data(self.address,0,3)
        tmp.insert(0,0)
        D2 = struct.unpack('>I',''.join([chr(c) for c in tmp]))[0]
        return D2


if '__main__' == __name__:

    bus = 1
    print('using bus {}'.format(bus))
    ms = MS5803_14BA(bus=bus)
    
    print(ms._C)
    print('raw pressure: {}'.format(ms._raw_pressure()))
    print('raw_temperature: {}'.format(ms._raw_temperature()))

    while True:
        #print('\x1b[2J\x1b[;H')
        print ms.pretty()
        time.sleep(0.1)

