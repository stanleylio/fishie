#!/usr/bin/python
import Adafruit_BBIO.GPIO as GPIO
import time

red_pin = 'P8_8'
yellow_pin = 'P8_10'
green_pin = 'P8_9'

def red_on():
    try:
        GPIO.output(red_pin,GPIO.HIGH)
    except:
        pass

def red_off():
    try:
        GPIO.output(red_pin,GPIO.LOW)
    except:
        pass

def yellow_on():
    try:
        GPIO.output(yellow_pin,GPIO.HIGH)
    except:
        pass

def yellow_off():
    try:
        GPIO.output(yellow_pin,GPIO.LOW)
    except:
        pass

def green_on():
    try:
        GPIO.output(green_pin,GPIO.HIGH)
    except:
        pass

def green_off():
    try:
        GPIO.output(green_pin,GPIO.LOW)
    except:
        pass

def usrx_on(x):
    try:
        assert x in [0,1,2,3]
        with open('/sys/class/leds/beaglebone:green:usr' + str(x) + '/brightness','w') as f:
            f.write('1')
    except:
        pass

def usrx_off(x):
    try:
        assert x in [0,1,2,3]
        with open('/sys/class/leds/beaglebone:green:usr' + str(x) + '/brightness','w') as f:
            f.write('0')
    except:
        pass

def indicators_setup():
    try:
        GPIO.setup(red_pin,GPIO.OUT)
        GPIO.setup(yellow_pin,GPIO.OUT)
        GPIO.setup(green_pin,GPIO.OUT)
        with open('/sys/class/leds/beaglebone:green:usr0/trigger','w') as f:
            f.write('none')
        with open('/sys/class/leds/beaglebone:green:usr1/trigger','w') as f:
            f.write('none')
        with open('/sys/class/leds/beaglebone:green:usr2/trigger','w') as f:
            f.write('none')
        with open('/sys/class/leds/beaglebone:green:usr3/trigger','w') as f:
            f.write('none')
        red_off()
        yellow_off()
        green_off()
        usr0_off()
        usr1_off()
        usr2_off()
        usr3_off()
    except:
        pass

def indicators_cleanup():
    try:
        GPIO.cleanup()
    except:
        pass

usr0_on = lambda: usrx_on(0)
usr0_off = lambda: usrx_off(0)
usr1_on = lambda: usrx_on(1)
usr1_off = lambda: usrx_off(1)
usr2_on = lambda: usrx_on(2)
usr2_off = lambda: usrx_off(2)
usr3_on = lambda: usrx_on(3)
usr3_off = lambda: usrx_off(3)


if '__main__' == __name__:
    indicators_setup()
    
    t = 0.5

    try:
        while True:
            print('red')
            red_on()
            yellow_off()
            green_off()
            usr0_off()
            usr1_off()
            usr2_off()
            usr3_off()
            time.sleep(t)

            print('yellow')
            red_off()
            yellow_on()
            green_off()
            usr0_off()
            usr1_off()
            usr2_off()
            usr3_off()
            time.sleep(t)

            print('green')
            red_off()
            yellow_off()
            green_on()
            usr0_off()
            usr1_off()
            usr2_off()
            usr3_off()
            time.sleep(t)

            print('usr0')
            red_off()
            yellow_off()
            green_off()
            usr0_on()
            usr1_off()
            usr2_off()
            usr3_off()
            time.sleep(t)

            print('usr1')
            red_off()
            yellow_off()
            green_off()
            usr0_off()
            usr1_on()
            usr2_off()
            usr3_off()
            time.sleep(t)

            print('usr2')
            red_off()
            yellow_off()
            green_off()
            usr0_off()
            usr1_off()
            usr2_on()
            usr3_off()
            time.sleep(t)

            print('usr3')
            red_off()
            yellow_off()
            green_off()
            usr0_off()
            usr1_off()
            usr2_off()
            usr3_on()
            time.sleep(t)
           
    except KeyboardInterrupt:
        print('user interrupted')

    indicators_cleanup()

