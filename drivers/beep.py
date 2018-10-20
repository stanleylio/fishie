import RPi.GPIO as GPIO
import time


def beep(on=0.1, off=0.9):
    pin = 18

    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(on)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(off)
        GPIO.cleanup(pin)
    except:
        GPIO.cleanup(pin)
        raise


if '__main__' == __name__:
    while True:
        try:
            beep()
        except KeyboardInterrupt:
            break
