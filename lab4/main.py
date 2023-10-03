from machine import *
import time
hspi = SPI(1, baudrate=80000000, polarity=0, phase=0)
v = Pin(12, Pin.IN)
while 1:
    print(v.value())
    time.sleep(0.1)