#!/usr/bin/python3
# Driver for the MS5837-30BA pressure sensor
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved
# 2017
import time, struct, traceback, io, fcntl


class MS5837_30BA:

    osr = {256:0,512:2,1024:4,2048:6,4096:8,8192:10}
    conv_time = {256:0.0006,512:0.00117,1024:0.00228,2048:0.00454,4096:0.00904,8192:0.01808}

    def __init__(self,address=0x76,bus=1):
        self.address = address
        self.fr = io.open('/dev/i2c-{}'.format(bus),'rb',buffering=0)
        self.fw = io.open('/dev/i2c-{}'.format(bus),'wb',buffering=0)
        I2C_SLAVE = 0x703   # but why?
        fcntl.ioctl(self.fr,I2C_SLAVE,self.address)
        fcntl.ioctl(self.fw,I2C_SLAVE,self.address)

        self.reset()
        self._C = self._read_prom()

    def __enter__(self):
        return self

    def __exit__(self,*ignored):
        return True

    def reset(self):
        self.fw.write(bytes([0x1E]))
        time.sleep(0.05)

    # {'p':kPa, 't':Deg.C}
    # OverSampling Rate (osr)
    # osr can be one of {256,512,1024,2048,4096,8192}
    def read(self,osr=8192):
        self._C = self._read_prom()
        
        D1 = self._raw_pressure(osr=osr)
        D2 = self._raw_temperature(osr=osr)
        C = self._C
        dT = D2 - C[5]*(2**8)
        TEMP = 2000 + dT*C[6]/(2**23)
        OFF = C[2]*(2**16) + (C[4]*dT)/(2**7)
        SENS = C[1]*(2**15) + (C[3]*dT)/(2**8)

        # - - -
        # "SECOND ORDER TEMPERATURE COMPENSATION" (P.9)
        if TEMP < 2000:
            Ti = 3*(dT**2)/(2**33)
            OFFi = 3*((TEMP - 2000)**2)/2
            SENSi = 5*((TEMP - 2000)**2)/(2**3)

            if TEMP < -1500:
                OFFi = OFFi + 7*((TEMP + 1500)**2)
                SENSi = SENSi + 4*((TEMP + 1500)**2)
        else:
            Ti = 2*(dT**2)/(2**37)
            OFFi = 1*((TEMP - 2000)**2)/(2**4)
            SENSi = 0

        OFF2 = OFF - OFFi
        SENS2 = SENS - SENSi
        TEMP2 = (TEMP - Ti)/100                         # Deg.C
        P2 = (((D1*SENS2)/(2**21) - OFF2)/(2**13))/10   # mbar

        TEMP = round(TEMP2,3)
        P = P2/10                                        # millibar to kilopascal
        P = round(P,3)
        return {'p':P,'t':TEMP}

    def pretty(self,r=None,*args,**kwargs):
        if r is None:
            r = self.read(*args,**kwargs)
        return '{} kPa, {} Deg.C'.format(r['p'],r['t'])

    def _read_prom(self):
        C = []
        for i in range(7):
            self.fw.write(bytes([0xA0 + 2*i]))
            C.append(self.fr.read(2))
        return [struct.unpack('>H',c)[0] for c in C]

    # uncompensated pressure, D1
    def _raw_pressure(self,osr=8192):
        self.fw.write(bytes([0x40 + self.osr[osr]]))
        time.sleep(self.conv_time[osr])
        self.fw.write(bytes([0]))
        tmp = bytearray(b'\0')
        tmp.extend(self.fr.read(3))
        return struct.unpack('>I',tmp)[0]

    # temperature, D2
    def _raw_temperature(self,osr=8192):
        self.fw.write(bytes([0x50 + self.osr[osr]]))
        time.sleep(self.conv_time[osr])
        self.fw.write(bytes([0]))
        tmp = bytearray(b'\0')
        tmp.extend(self.fr.read(3))
        return struct.unpack('>I',tmp)[0]


if '__main__' == __name__:

    bus = 1
    print('using bus {}'.format(bus))
    ms = MS5837_30BA(bus=bus)
    
    print(ms._C)
    #print('raw pressure: {}'.format(ms._raw_pressure()))
    #print('raw_temperature: {}'.format(ms._raw_temperature()))

    while True:
        #print('\x1b[2J\x1b[;H')
        print(ms.pretty(osr=256))
        time.sleep(0.1)

