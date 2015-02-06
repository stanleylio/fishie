import Adafruit_BBIO.ADC as ADC
from Adafruit_BMP085 import BMP085
from datetime import datetime
import time

# Once in production it shouldn't be called "sandbox" anymore... I usually delete the
# sandbox code during refactoring.

# Print 10 lines of BMP180 and ADC readings along with timestamps, as a demo of:
# 	The Adafruit_BBIO library (without dto)
#	Accessing multiple sensors within one python script
#	Timestamping
#
# BMP180 on I2C2 (pin 19,20)
# AIN0 on pin 39
# AIN5 on pin 36
#
# Stanley Hou In Lio, hlio@usc.edu
# All Rights Reserved. February 2015

ADC.setup()
bmp = BMP085(0x77,3)  # ULTRAHIRES Mode

Avcc = 1.8

print 'Timestamp, Temperature, Pressure, Altitude, AIN0 voltage, AIN5 voltage, Wind Speed'

try:
    with open('sandbox3_output.txt','w',0) as f:
        while True:
            ts = time.time()
            ts = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            temperature = bmp.readTemperature()
            pressure = bmp.readPressure()
            #altitude = bmp.readAltitude()

            v0 = ADC.read('AIN0')*Avcc
            v5 = ADC.read('AIN5')*Avcc

            # ******
            # As stated in the email, the mapping to wind speed is
            #   0-2VDC == 0-32.4m/s
            # Be mindful that the ADC can only accept up to 1.8V. Higher voltage may
            # damage the BBB. If the input is indeed up to 2V, a voltage divider is
            # required.
            #
            # read_raw() is not recommended. Adafruit's idea of "raw" is kinda funny/wrong.
            # It returns a float close to 1800.0 at full swing, whereas the common meaning
            # of "ADC raw" is an unsigned integer read straight out of the register in
            # the native resolution of the ADC. In the case of the BBB (12-bit) "raw" should
            # be an integer in [0,2^12-1] = [0,4095].
            #
            # Furthermore, it doesn't even output 1800.0 at full swing (but a number slightly
            # less than that). The library introduces another source of error itself.
            #windSpeed = ADC.read_raw('P9_36')*0.0202 - 7.99
            # shouldn't it be like this?
            windSpeed = v5/2.*32.4

            s = '{},{:.1f}C,{:.2f}hPa,{:.3f}v,{:.3f}v,{:.2f}m/s'.\
            format(ts,temperature,pressure/100.0,v0,v5,windSpeed)
            print s
            f.write(s + '\n')
            f.flush()

            time.sleep(1)
except KeyboardInterrupt:
    print 'user interrupted'

