from Adafruit_I2C import Adafruit_I2C
from Adafruit_ADS1x15 import ADS1x15
from numpy import mean,amax
from threading import Thread,Event
import time

# new thing learned: Python name mangling.
# http://stackoverflow.com/questions/8689964/python-why-do-some-functions-have-underscores-before-and-after-the-functio
# https://docs.python.org/2/tutorial/classes.html


# the adafruit class does not take I2C bus ID as input
# override its __init__ here to use I2C1 (pin 17,18, most likely mapped /dev/i2c-2)
class ADS1115_I2C1(ADS1x15):
    def __init__(self):
        self.address = 0x48
        self.i2c = Adafruit_I2C(self.address,busnum=2)
        self.debug = False
        self.ic = self._ADS1x15__IC_ADS1115
        self.pga = 6144


class Anemometer(Thread):
    def __init__(self):
        super(Anemometer,self).__init__()
        self._adc = ADS1115_I2C1()
        self._readings = []

        # thread related
        self._stop = Event()
        self.daemon = True
        self.start()

    def read(self):
        if len(self._readings) <= 0:
            return None
        tmp = {'average':mean(self._readings),'gust':amax(self._readings)}
        tmp = {k:float('{:.2f}'.format(tmp[k])) for k in tmp.keys()}    # keep 2 decimal places
        self._readings = []     # avg and gust between consecutive reads
        return tmp

    def run(self):
        while not self._stop.is_set():
            #print 'alive'
            tmp = self._adc.readADCSingleEnded(channel=1,pga=4096,sps=250)/1000.    # in V
            tmp = max(tmp*20.25 - 8.1,0)
            self._readings.append(tmp)
            # max 60 min worth, just a cap on memory usage
            # could have stored just the max, sum and N instead (avg=sum/N)
            while len(self._readings) > 60*60:
                self._readings.pop(0)
            time.sleep(1)

    def stop(self):
        self._stop.set()

    def is_running(self):
        return not self._stop.is_set()


if '__main__' == __name__:
    
    try:
        an = Anemometer()
        while True:
            tmp = an.read()
            if tmp is not None:
                print 'avg={:.1f} m/s, gust={:.1f} m/s'.format(tmp['average'],tmp['gust'])
            time.sleep(5)
    except KeyboardInterrupt:
        print 'user interrupted'
    
