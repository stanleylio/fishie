import serial,logging


class RMY85106:
    def __init__(self,port,baud=9600):
        self._s = serial.Serial(port,baud,timeout=0.1)

    def __del__(self):
        try:
            self._s.close()
        except:
            pass

    def read(self):
        #self._s.write('M0!\r')       # the sensor is slow at processing commands...
        for c in 'M0!\r':
            self._s.write(c)
            self._s.flushOutput()
        line = []
        for i in range(20):     # should be ~17 chr
            c = self._s.read(size=1)
            if len(c):
                line.extend(c)
            if c == '\r':
                break
        #logger.debug(''.join(line))
        #logger.debug([ord(c) for c in line])
        if len(line) <= 0:
            logging.warning('No response from ultrasonic anemometer')
            return

        line = ''.join(line).strip().split(' ')
        if not ('0' == line[0] and '*' == line[3][2]):    # '0' is the address of the sensor
            logging.warning('Unexpected response from ultrasonic anemometer: {}'.format(line))
            return
        
        return {'v':float(line[1]),'d':float(line[2])}


if '__main__' == __name__:
    import time
    
    rmy = RMY85106('/dev/ttyUSB4')
    while True:
        print rmy.read()
        time.sleep(0.1)
