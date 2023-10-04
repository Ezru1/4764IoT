from machine import *
import time

global T
T = -1


def callback(p):
    global T
    t = time.ticks_ms()
    if t < T + 100:
        return
    T = t
    print("Interrupt!")


button = Pin(14, Pin.IN)
button.irq(trigger=Pin.IRQ_FALLING, handler=callback)

while 1:
    pass
