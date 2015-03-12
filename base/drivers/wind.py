from __future__ import with_statement   # always something new to learn...
import Adafruit_BBIO.ADC as ADC
import time,math

# Wind speed "sensor" wrapper

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

class Anemometer:
    Avcc = 1.8
    
    def __init__(self):
        #print '__init__'
        ADC.setup()

    def __enter__(self):
        #print '__enter__'
        return self

    def __exit__(self,*ignored):
        #print '__exit__'
        return True

    def read(self):
        v5 = ADC.read('AIN5')*self.Avcc
        # if I forget the self., this thing will terminate without throwing any
        # warning message. weird. context switched? but there is no global Avcc
        # so why doesn't it complain?
        #v5 = ADC.read('AIN5')*Avcc
        #return v5/2.*32.4
        # the god of MATLAB has spoken...
        #polyfit([0.397 2],[0 32.4],1)
        return max(v5*20.2121 - 8.0242,0)

if '__main__' == __name__:
    '''an = Anemometer()
    for i in range(10):
        print an.read()
        time.sleep(1)
        '''

    try:
        with Anemometer() as an:    # this thing eats all my exceptions...
            while True:
                tmp = an.read()
                print '{:.1f} m/s'.format(tmp)
                # why doesn't it complain about missing library and incorrect use of *?
                time.sleep(0.5)
    except KeyboardInterrupt:
        print 'user interrupted'
    
