#!/usr/bin/python3
# Stanley H.I. Lio
import smbus, time, struct, traceback, logging


class VEML6040:

    ITms = {40:0, 80:0b001, 160:0b010, 320:0b011, 640:0b100, 1280:0b101}

    def __init__(self,address=0x10,bus=1):
        self.address = address
        self.i2c = smbus.SMBus(bus)

        time.sleep(0.0025)

        self.config = 0
        self._write_config()

    def set_mode_auto(self,auto):
        if auto:
            self.config &= 2
        else:
            self.config |= 0b00000010
        self._write_config()
        return self

    def enable_sensor(self):
        self.config &= 0b11111110
        self._write_config()
        return self
    
    def disable_sensor(self):
        self.config |= 1
        self._write_config()
        return self
    
    def set_integration_time(self,it):
        """set integration time to it millisecond"""
        assert it in self.ITms
        self.config &= 0b10001111
        self.config |= self.ITms[it] << 4
        self._write_config()
        return self

    def read(self):
        return {'r':self._read(0x8),
                'g':self._read(0x9),
                'b':self._read(0xA),
                'w':self._read(0xB),
                }

    def _write(self, command, lsb, msb):
        self.i2c.write_i2c_block_data(self.address, command, [lsb,msb])

    def _read(self, command):
        #self.i2c.write_i2c_block_data(self.address, command, [0])
        self.i2c.write_byte(self.address, command)
        data = self.i2c.read_i2c_block_data(self.address, command, 2)
        return data[0] + (data[1] << 8)

    def _write_config(self):
        self._write(0, self.config & 0xFF, 0)

    def __enter__(self):
        return self

    def __exit__(self, *ignored):
        return True


if '__main__' == __name__:

    bus = 1
    print('using bus {}'.format(bus))

    while True:
        try:
            veml = VEML6040(bus=bus)
            veml.enable_sensor().set_mode_auto(True).set_integration_time(40)
            print(veml.read())
        except IOError:
            logging.exception('Cant\'t reach sensor on bus {}'.format(bus))
        except KeyboardInterrupt:
            break
        time.sleep(0.1)
