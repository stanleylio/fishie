from Adafruit_ADS1x15 import ADS1x15
from scipy.signal import medfilt
from numpy import mean
import time

class Anemometer(object):
    def __init__(self):
        ADS1115 = 0x01	# 16-bit ADC
        self._adc = ADS1x15(ic=ADS1115,debug=True)

    def read(self):
        v = []
        for i in range(20):
            tmp = self._adc.readADCSingleEnded(channel=1,pga=4096,sps=250)/1000.    # in V
            v.append(tmp)
        v = mean(mean(medfilt(v,5)))
        # Thus Spoke MATLAB: polyfit([.4 2],[0 32.4],1)
        # see also: https://www.adafruit.com/product/1733
        return max(v*20.25 - 8.1,0)


if '__main__' == __name__:
    
    try:
        an = Anemometer()
        while True:
            tmp = an.read()
            print '{:.1f} m/s'.format(tmp)
            #print tmp
            time.sleep(0.5)
    except KeyboardInterrupt:
        print 'user interrupted'
    
