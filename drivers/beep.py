import RPi.GPIO as GPIO
import time


def beep(on=0.1, off=0.9, autocleanup=True):
    pin = 18

    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(on)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(off)
        if autocleanup:
            GPIO.cleanup()
    except:
        if autocleanup:
            GPIO.cleanup()
        raise


if '__main__' == __name__:
    while True:
        try:
            beep(autocleanup=True)
        except KeyboardInterrupt:
            break
