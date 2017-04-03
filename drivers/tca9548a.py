# Select (or deselect) an I2C channel using the TCA9548A
#
# Example: python tca9548a.py 0 to select CH0
#
# 
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved, 2017
# University of Hawaii

from smbus import SMBus


class TCA9548A:

    def __init__(self,bus=1,addr=0x70):
        self._addr = addr
        self._bus = SMBus(bus=bus)

    def use_channel(self,ch):
        """If ch is in {0..7}, select channel ch; if ch is None, deselect all channels."""
        if ch is None:
            # Deselect all/any channel
            self._bus.write_byte(self._addr,0)
            return
            
        if ch not in range(8):
            raise ValueError('Channel must be one of {0,1,2,3,4,5,6,7}')
        self._bus.write_byte(self._addr,1 << ch)

    # the mux allows fan-out/fan-in. use at own risk
    def use_channel_combo(self,chs):
        self._bus.write_byte(self._addr,chs)


if '__main__' == __name__:
    import sys

    if len(sys.argv) <= 1:
        print('To use channel N: python tca9548a.py N, where N is one of {0,1,2,3,4,5,6,7}')
    mux = TCA9548A(bus=1,addr=0x70)
    mux.use_channel(int(sys.argv[1]))
