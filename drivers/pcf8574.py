import io, fcntl, logging, sys


class PCF8574:
    _state = [False]*8

    def __init__(self, *, address=0x20):
        self._fr = io.open('/dev/i2c-1', 'rb', buffering=0)
        self._fw = io.open('/dev/i2c-1', 'wb', buffering=0)
        I2C_SLAVE = 0x703
        fcntl.ioctl(self._fr, I2C_SLAVE, address)
        fcntl.ioctl(self._fw, I2C_SLAVE, address)

    def set_pin(self, ch, state):
        assert ch in range(8)
        assert state in [True, False]

        self._state[ch] = state
        self._set_output()

    def set_port(self, states):
        assert 8 == len(states)
        assert all([type(state) is bool for state in states])
        
        self._state = list(states)
        self._set_output()

    def _set_output(self):
        x = sum([(1 if self._state[k] else 0) << k for k in range(8)])
        self._fw.write(bytes([x, x]))
    

if '__main__' == __name__:

    import time

    iomux = PCF8574(address=0x20)

    try:    
        while True:
            for i in range(8):
                iomux.set_pin(i, False)

            for i in range(8):
                iomux.set_pin(i, True)
                time.sleep(0.1)
    except:
        logging.exception('?')

        iomux.set_port([False for _ in range(8)])
