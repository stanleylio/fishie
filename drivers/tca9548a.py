# Select (or deselect) an I2C channel using the TCA9548A
#
# Example: python3 tca9548a.py 0 to select CH0
#
# How the mux works: the mux has its own I2C address (0x70,0x71...).
# It uses the last byte you send to it to control which channel connects
# to the master I2C. Each bit in that byte corresponding to each channel.
# (i.e. it allows fan-in/out when more than one bit is set)
#
# After a channel(s) is connected to the master I2C bus, all I2C traffic
# is transparent (as long as it doesn't collide with 0x70, or wherever
# the mux is at.)
#
# The {A0,A1,A2} pins of the mux controls the mux's own address, NOT the
# channel to use. The mux is only "transparent" as long as the I2C traffic
# doesn't address the mux itself.
# 
# Stanley H.I. Lio
from smbus import SMBus


class TCA9548A:

    def __init__(self, bus=1, addr=0x70):
        self._addr = addr
        self._bus = SMBus(bus=bus)

    def use_channel(self, ch):
        """If ch is in {0..7}, select channel ch; if ch is None, deselect all channels."""
        if ch is None:
            # Deselect all/any channel
            self._bus.write_byte(self._addr, 0)
            return
            
        if ch not in range(8):
            raise ValueError('Channel must be one of {0,1,2,3,4,5,6,7}')
        self._bus.write_byte(self._addr, 1 << ch)

    # the mux allows fan-out/fan-in. use at own risk
    def use_channel_combo(self, chs):
        self._bus.write_byte(self._addr, chs)


if '__main__' == __name__:
    import sys

    if len(sys.argv) <= 1:
        print('To use channel N: python tca9548a.py N, where N is one of {0,1,2,3,4,5,6,7}')
    mux = TCA9548A(bus=1, addr=0x70)
    mux.use_channel(int(sys.argv[1]))
