#!/usr/bin/python
import Adafruit_BBIO.GPIO as GPIO
import time

red_pin = 'P8_8'
green_pin = 'P8_9'

GPIO.setup(red_pin,GPIO.OUT)
GPIO.setup(green_pin,GPIO.OUT)

t = 0.5

try:
    while True:
        print('red')
        GPIO.output(red_pin,GPIO.HIGH)
        GPIO.output(green_pin,GPIO.LOW)
        time.sleep(t)
        print('green')
        GPIO.output(red_pin,GPIO.LOW)
        GPIO.output(green_pin,GPIO.HIGH)
        time.sleep(t)
except KeyboardInterrupt:
    print 'user interrupted'

GPIO.cleanup()
