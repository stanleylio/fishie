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
# AIN5 on pin 36
#
# Stanley Hou In Lio, hlio@usc.edu
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

print 'Timestamp, Temperature, Pressure, Altitude, AIN0 voltage, AIN5 voltage'

with open('sandbox1_output.txt','w') as f:
	for i in range(30):
		timestamp = get_timestamp()
		
		temperature = bmp.readTemperature()
		pressure = bmp.readPressure()
		altitude = bmp.readAltitude()
		
		v0 = ADC.read('AIN0')
		v5 = ADC.read('AIN5')
		windSpeed = ADC.read_raw("P9_36")*0.0202-7.99

		s = '{},{:.1f}C,{:.2f}hPa,{:.2f}m,{:.3f}v,{:.3f}v,{:.2f}m/s'.\
		format(timestamp,temperature,pressure/100.0,altitude,v0*1.8,v5,windSpeed)
		print s
		f.write(s + '\n')
		
		time.sleep(1)

