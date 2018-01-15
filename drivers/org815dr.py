import serial,logging
from datetime import datetime


class ORG815DR:
    last_reset_day = datetime.utcnow().day
    
    def __init__(self,port,baud=1200):
        self._s = serial.Serial(port,baud,timeout=0.1)

    def __del__(self):
        try:
            self._s.close()
        except:
            pass

    def read(self):
        self._s.write('A'.encode())
        line = []
        for i in range(30):
            c = self._s.read(size=1)
            if len(c):
                line.append(c.decode())
            if '\r' == c:
                break
        if len(line) <= 0:
            logging.warning('No response from optical rain gauge')
            return
        line = ''.join(line).rstrip()
        logging.debug(line)
        return {'weather_condition':line[0:2],
                'instantaneous_mmphr':float(line[3:7]),
                'accumulation_mm':float(line[8:15])}

    def reset_accumulation_if_required(self):
        # reset accumulation once past UTC midnight
        dt = datetime.utcnow()
        if not dt.day == self.last_reset_day:
            logging.info('Accumulation Data Reset')
            self._s.write('R'.encode())
            for i in range(10):
                r = self._s.read()
                if len(r):  # whatever it is, as long as the sensor responded
                    self.last_reset_day = dt.day
                    break


if '__main__' == __name__:
    import time, logging

    logging.basicConfig(level=logging.DEBUG)
    
    org = ORG815DR('/dev/ttyUSB6')
    while True:
        print(org.read())
        org.reset_accumulation_if_required()
        time.sleep(0.1)
