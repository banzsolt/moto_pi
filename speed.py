import RPi.GPIO as GPIO
import time

class Translator:

    _tens = [40, 38, 37, 36]
    _lastDigits =[3, 5, 7, 12, 11, 13, 15, 16]

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        for pin in self._tens:
            GPIO.setup(pin, GPIO.OUT)
        for pin in self._lastDigits:
            GPIO.setup(pin, GPIO.OUT)

    def parse(self, number):
        for x in range(0, number % 10):
            GPIO.output(self._lastDigits[x], GPIO.HIGH)
        for x in range(0, number / 10):
            GPIO.output(self._tens[x], GPIO.HIGH)