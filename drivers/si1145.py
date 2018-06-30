import logging, time, io, fcntl, struct


logger = logging.getLogger(__name__)


class Si1145:
    
    # I2C register addresses (P.29)
    PART_ID =       0x0
    REV_ID =        0x1
    SEQ_ID =        0x2
    HW_KEY =        0x7
    PARAM_WR =      0x17
    COMMAND =       0x18
    RESPONSE =      0x20
    IRQ_STATUS =    0x21
    ALS_VIS_DATA =  0x22
    ALS_IR_DATA =   0x24
    AUX_DATA =      0x2C
    PARAM_RD =      0x2E

    # RAM addresses (P.45)
    CHLIST = 0x01
    ALS_IR_ADCMUX = 0x0E
    ALS_IR_ADC_GAIN = 0x1E
    ALS_IR_ADC_MISC = 0x1F
    ALS_VIS_ADC_GAIN = 0x11
    ALS_VIS_ADC_MISC = 0x12
    
    def __init__(self, bus=1, address=0x60):
        self.address = address
        self.fr = io.open('/dev/i2c-{}'.format(bus), 'rb',buffering=0)
        self.fw = io.open('/dev/i2c-{}'.format(bus), 'wb',buffering=0)
        I2C_SLAVE = 0x703   # but why?
        fcntl.ioctl(self.fr, I2C_SLAVE, self.address)
        fcntl.ioctl(self.fw, I2C_SLAVE, self.address)

        self.reset()
        self._write(self.HW_KEY, 0x17)   # magic, don't ask why.
        self.enable()

    def check_ID(self):
        r = self._read(self.PART_ID)[0]
        if 0x45 != r:
            return False
        r = self._read(self.REV_ID)[0]
        if 0 != r:
            return False
        r = self._read(self.SEQ_ID)[0]
        if 8 != r:
            return False
        return True

    def read_raw(self):
        try:
            #self._write(self.COMMAND, 0)
            #if not 0 == self._read(self.RESPONSE)[0] & 0xF0:        # top nibble indicates error. bottom nibble is roll over counter
            #    logging.debug('Operation error')
            #    return
            self._write(self.COMMAND, 0b00000110)    # P.23 ALS_FORCE
            time.sleep(0.0005)
            r = {}
            r['visible'] = struct.unpack('<H', self._read(self.ALS_VIS_DATA, length=2))[0]
            r['ir'] = struct.unpack('<H', self._read(self.ALS_IR_DATA, length=2))[0]
            r['uv'] = struct.unpack('<H', self._read(self.AUX_DATA, length=2))[0]
            return r
        except IOError as e:
            logging.debug('Read error')
        return

    def read(self):
        """visible light and IR light in lux; assumes small IR diode, sunlight.
Data sheet claims a 14.5x reduction in High Range mode, but experiments show a ~8.5x for IR and ~3.2x for visible light.
Si1145 is obsolete now, not spending more time fixing this."""
        try:
            r = self.read_raw()
            r['visible'] = round(r['visible']*self.vis_multiplier, 3)
            r['ir'] = round(r['ir']*self.ir_multiplier, 3)
            r['uv'] = round(r['uv']/100, 1)
            return r
        except IOError as e:
            logger.debug(e)
        return None

    def reset(self):
        self._write(self.COMMAND, 0)
        if not 0 == self._read(self.RESPONSE)[0] & 0xF0:        # top nibble indicates error. bottom nibble is roll over counter
            logging.error('Si1145::reset() failed')
            return
        self._write(self.COMMAND, 1)                            # P.22 Table 5
        self.vis_multiplier = 1/0.282                           # assumes sunlight; consult P.6
        self.ir_multiplier = 1/2.44                             # assumes sunlight; consult P.7
        time.sleep(0.005)    # > 1ms

    def high_signal_range(self):
        # choice of two IR photodiodes: small vs. large
        self.set_param(self.ALS_IR_ADCMUX, 0)                   # P.55 (small IR photodiode)
        #self.set_param(self.ALS_IR_ADCMUX, 3)                   # P.55 (large IR photodiode)

        # increase ADC integration time by 2**ALS_IR_ADC_GAIN times
        self.set_param(self.ALS_IR_ADC_GAIN, 0)                 # P.59

        # further divide gain by 14.5
        tmp = self.query_param(self.ALS_IR_ADC_MISC)            # P.59 read-modify-write as required
        self.set_param(self.ALS_IR_ADC_MISC, tmp | (1 << 5))    # P.59 High Signal Range (gain divided by 14.5)

        self.ir_multiplier = 1/(2.44/14.5)                      # assumes sunlight; consult P.7

        # increase ADC integration time by 2**ALS_VIS_ADC_GAIN times
        self.set_param(self.ALS_VIS_ADC_GAIN, 0)                # P.57 (/1)
        self.set_param(self.ALS_VIS_ADC_MISC, 1 << 5)           # P.57 High Signal Range (gain divided by 14.5)

        self.vis_multiplier = 1/(0.282/14.5)                    # assumes sunlight; consult P.6

    def enable(self):
        self._write(0x13, 0x7B)                                 # P.16 UV stuff
        self._write(0x14, 0x6B)
        self._write(0x15, 1)
        self._write(0x16, 0)
        return self.set_param(self.CHLIST, 0xF0)                # P.47

    def query_param(self, param):
        """Read a RAM parameter
        param: RAM address of the parameter"""
        self._write(self.COMMAND, 0)
        if not 0 == self._read(self.RESPONSE)[0] & 0xF0:        # top nibble indicates error. bottom nibble is roll over counter
            logging.error('Si1145::query_param() failed')
            return
        self._write(self.COMMAND,0x80 | param)                  # PARAM_QUERY, P.22
        for i in range(25):
            time.sleep(0.001)
            if not 0 == self._read(self.RESPONSE):
                break
        return self._read(self.PARAM_RD)[0]

    def set_param(self, param, val):
        """Set a RAM parameter
        param: RAM address of the parameter
        val: value to be written"""
        self._write(self.PARAM_WR, val)                         # put val in "mailbox" register PARAM_WR
        self._write(self.COMMAND, 0)
        if not 0 == self._read(self.RESPONSE)[0] & 0xF0:        # top nibble indicates error. bottom nibble is roll over counter
            logging.error('Si1145::set_param() failed')
            return
        self._write(self.COMMAND, 0xA0 | param)                 # PARAM_SET, P.22
        for i in range(25):
            time.sleep(0.001)
            if not 0 == self._read(self.RESPONSE)[0] & 0xF0:    # top nibble indicates error. bottom nibble is roll over counter
                break
        return self._read(self.PARAM_RD)[0]

    def _read(self, reg, *_, length=1):
        #return self.bus.read_byte_data(self.address, reg)
        self.fw.write(bytes([reg]))
        return self.fr.read(length)

    def _write(self, r, v):
        #self.bus.write_byte_data(self.address, r, v)
        self.fw.write(bytes([r, v]))


if '__main__' == __name__:
    
    s = Si1145(bus=1)
    
    assert s.check_ID()

    s.high_signal_range()
    
    while True:
        try:
            #print(s.read())
            print(s.read_raw())
            time.sleep(0.1)
        except IOError:
            pass
        except KeyboardInterrupt:
            print('user interrupted')
            break

