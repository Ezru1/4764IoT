from machine import *
import ssd1306
import time
from math import *
from config import *

def f(mx, x):  # linear map
    print(int((x - 5) * (255 / (mx - 5))))
    return max(int((x - 5) * (255 / (mx - 5))), 0)

adc = ADC(0)
mx = 0  # adaptive
for i in range(1000):
    mx = max(mx, adc.read())

while 1:
    print(adc.read())
    time.sleep(0.05)