from machine import Pin
import utime

red = Pin(0, Pin.OUT)
for k in range(10**9):
    t = 1 if (k // 6) % 3 == 1 else 0.5
    red.value(k % 2)
    utime.sleep(t)

    if not (k + 1) % 18:  # interval
        utime.sleep(2)
