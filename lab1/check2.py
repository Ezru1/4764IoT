from machine import Pin
import utime

red, blue = Pin(0, Pin.OUT), Pin(2, Pin.OUT)
while 1:
    for i in range(10):
        red.value(i // 5 % 2)
        blue.value(i % 2)
        utime.sleep(0.1)
