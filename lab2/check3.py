from machine import *

import utime
import time

global T1, T2
T1, T2 = -1, -1


def strt(p):
    global T1
    t = time.ticks_ms()
    if t < T1 + 100:
        return
    T1 = t
    print("InterruptFALLING!")


def end(p):
    global T2
    t = time.ticks_ms()
    if t < T2 + 100:
        return
    T2 = t
    print("InterruptRISING!")


Fal = Pin(14, Pin.IN)
Ris = Pin(12, Pin.IN)
Fal.irq(trigger=Pin.IRQ_FALLING, handler=strt)
Ris.irq(trigger=Pin.IRQ_RISING, handler=end)
led = PWM(Pin(13, Pin.OUT), freq=1000)
adc = ADC(0)

mx = 0  # adaptive
for i in range(100):
    mx = max(mx, adc.read())


def f(mx, x):  # linear map
    return 1024 - int(x * (1024 / mx))


for i in range(10**9):
    x = adc.read()
    if Fal.value():
        led.duty(0)
    else:
        led.duty(f(mx, x))
    utime.sleep(0.01)  # sample interval
