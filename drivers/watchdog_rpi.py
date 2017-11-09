#!/usr/bin/python
# watchdog driver for RPi
# I2C code lifed from Atlas Scientific's code to deal with RPi's I2C bug
# source: https://github.com/AtlasScientific/Raspberry-Pi-sample-code/blob/master/i2c.py
# Stanley H.I. Lio
# hlio@hawaii.edu
import io,fcntl,struct,logging,traceback


logger = logging.getLogger(__name__)


class Watchdog:
    """Driver for watchdog (RPi version)"""
    def __init__(self,addr=0x51):
        self.addr = addr
        self.fr = io.open('/dev/i2c-1','rb',buffering=0)
        self.fw = io.open('/dev/i2c-1','wb',buffering=0)
        I2C_SLAVE = 0x703
        fcntl.ioctl(self.fr,I2C_SLAVE,addr)
        fcntl.ioctl(self.fw,I2C_SLAVE,addr)

    def reset(self):
        return self.read(0xA)
       
    def wdt_fired(self):
        return self.read(0xC)

    def read_vbatt(self):
        return self.read(0xE)

    def read(self,reg):
        self.fw.write(chr(reg))
        r = self.fr.read(2)
        r = ''.join([chr(ord(c) & ~0x80) for c in r])   # that mask == RPi hack
        return struct.unpack('<H',r)[0]     # little endian, uint16_t

    def close(self):
        self.fr.close()
        self.fw.close()


def reset_auto():
    good = False
    try:
        w = Watchdog()
        counter = w.reset()
        logging.debug('counter={}'.format(counter))
        if counter >= 0 and counter <= 5*60:
            good = True
    except IOError:
        #logging.exception(traceback.format_exc())
        pass
    if good:
        logger.debug('Found watchdog.')
        return True
    else:
        logger.warning('No WDT found.')
        return False


if '__main__' == __name__:
    logging.basicConfig(level=logging.DEBUG)
    #reset_auto()

    w = Watchdog()
    while True:
        print(w.read_vbatt())
