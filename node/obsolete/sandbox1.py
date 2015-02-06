import Adafruit_BBIO.ADC as ADC
from Adafruit_BMP085 import BMP085
import datetime
import time

# Print 10 lines of BMP180 and ADC readings along with timestamps, as a demo of:
# 	The Adafruit_BBIO library (without dto)
#	Accessing multiple sensors within one python script
#	Timestamping
#
# BMP180 on I2C2 (pin 19,20)
# AIN0 on pin 39
# 
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. December 2014

# returns a time stamp string
def get_timestamp(d=None):
    if None == d:
        d = datetime.datetime.now()
    timestamp = '{:02d}{:02d}{:02d}-{:02d}{:02d}{:02d}'.\
                format(d.year,d.month,d.day,d.hour,d.minute,d.second)
    return timestamp


ADC.setup()
bmp = BMP085(0x77,3)  # ULTRAHIRES Mode

print 'Timestamp, Temperature, Pressure, Altitude, AIN0 voltage'

with open('sandbox1_output.txt','w') as f:
    for i in range(10):
        timestamp = get_timestamp()

        temperature = bmp.readTemperature()
        pressure = bmp.readPressure()
        altitude = bmp.readAltitude()

        v = ADC.read('AIN0')
        s = '{},{:.1f}C,{:.2f}hPa,{:.2f}m,{:.3f}v'.\
        format(timestamp,temperature,pressure/100.0,altitude,v*1.8)
        print s
        f.write(s + '\n')

        time.sleep(1)

