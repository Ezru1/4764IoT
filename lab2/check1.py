from machine import *
import utime

led = PWM(Pin(13, Pin.OUT), freq=1000)
adc = ADC(0)

mx = 0  # adaptive
for i in range(100):
    mx = max(mx, adc.read())


def f(mx, x):  # linear map
    return 1024 - int(x * (1024 / mx))


for i in range(10**9):
    x = adc.read()
    led.duty(f(mx, x))
    utime.sleep(0.01)  # sample interval
