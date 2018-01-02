'''import smbus, time


i2c = smbus.SMBus(1)

address = 0x48

command = 0
lsb = 0
msb = 0
i2c.write_i2c_block_data(address, command, [lsb,msb])

command = 4
while True:
    i2c.write_i2c_block_data(address, command, [0])
    data = i2c.read_i2c_block_data(address, command, 2)
    print(data)
    
    time.sleep(0.1)







exit()'''






#!/usr/bin/python3
# Driver for VEML6030 ambient light sensor
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved
# 2017
import smbus, time, struct, traceback


class VEML6030:

    ALS_GAIN = {1:0, 2:1, 1/8:0b10, 1/4:0b11}
    ALS_IT = {25:0b1100, 50:0b1000, 100:0, 200:1, 400:0b10, 800:0b11}
    ALS_PES = {1:0, 2:1, 4:2, 8:3}

    def __init__(self,address=0x48,bus=1):
        self.address = address
        self.i2c = smbus.SMBus(bus)
        # This won't do. It doesn't do Repeated Start.
        #self.fr = io.open('/dev/i2c-{}'.format(bus),'rb',buffering=0)
        #self.fw = io.open('/dev/i2c-{}'.format(bus),'wb',buffering=0)
        #I2C_SLAVE = 0x703
        #I2C_RDWR = 0x707   # this throws some error about "unknown address"
        #fcntl.ioctl(self.fr,I2C_SLAVE,self.address)
        #fcntl.ioctl(self.fw,I2C_SLAVE,self.address)

        time.sleep(0.0025)

        self.config = 0
        self._write_config()

    def set_gain(self,gain):
        assert gain in self.ALS_GAIN
        self.config &= 0b1110011111111111
        self.config |= self.ALS_GAIN[gain] << 11
        self._write_config()
        return self

    def set_integration_time(self,itms):
        assert itms in self.ALS_IT
        self.config &= 0b1111110000111111
        self.config |= self.ALS_IT[itms] << 6
        self._write_config()
        return self

    def set_ALS_persistence(self,pers):
        assert pers in self.ALS_PES
        self.config &= 0b1111111111110011
        self.config |= self.ALS_PES[pers] << 2
        self._write_config()
        return self

    def set_psm(self):
#!! WHAT?
        self._write(3,0b0,0)
        return self

    def power_on(self):
        self.config &= 0b1111111111111110
        self._write_config()
        return self

    def shutdown(self):
        self.config |= 1
        self._write_config()
        return self

    def _write(self, command, lsb, msb):
        self.i2c.write_i2c_block_data(self.address, command, [lsb,msb])

    def _read(self, command):
        self.i2c.write_byte(self.address, command)
        data = self.i2c.read_i2c_block_data(self.address, command, 2)
        return data[0] + (data[1] << 8)

    def _write_config(self):
        self._write(0, self.config & 0xFF, (self.config >> 8) & 0xFF) 

    def __enter__(self):
        return self

    def __exit__(self, *ignored):
        return True


if '__main__' == __name__:

    bus = 1
    print('using bus {}'.format(bus))
    veml = VEML6030(bus=bus)
    veml.power_on()
    veml.set_integration_time(100)
    veml.set_gain(1)
    veml.set_psm()
    time.sleep(1)
    

    while True:
        print(veml._read(4))
        time.sleep(0.1)
