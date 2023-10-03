from machine import *
import ssd1306
import time
from math import *
from config import *

class button:
    def __init__(self,pin,irqfunc):
        self.btn = Pin(pin, Pin.IN)
        self.btn.irq(trigger=Pin.IRQ_FALLING, handler=irqfunc)

def zeropad(k):
    if k < 10:
        return "0" + str(k)
    return str(k)

def f(mx, x):  # linear map
    print(int((x - 5) * (255 / (mx - 5))))
    return max(int((x - 5) * (255 / (mx - 5))), 0)

def show(a, b, c, k, cnt, blink, ena):
    display.fill(0)
    color = 1
    enb = cnt // k % 2
    if not ena or enb:
        display.rect(51, 21, 2, 2, color)
        display.rect(51, 24, 2, 2, color)
        display.rect(71, 21, 2, 2, color)
        display.rect(71, 24, 2, 2, color)
    if not (blink == 1 or ena) or enb:
        display.text(zeropad(a), 34, 20, color)
    if not (blink == 2 or ena) or enb:
        display.text(zeropad(b), 54, 20, color)
    if not (blink == 3 or ena) or enb:
        display.text(zeropad(c), 74, 20, color)
    if not blink == 4 or enb:
        display.text(str(Year)+'-', 0, 0, color)
    if not blink == 5 or enb:
        display.text(DM[Month]+'-', 40, 0, color)
    if not blink == 6 or enb:
        display.text(zeropad(Day), 72, 0, color) 
    display.text(DW[Week], 0, 20, color)
    if enb:display.contrast(f(mx, adc.read()));print(adc.read())
    display.show()
    return

def Select_a(p):  # 可以传参吗？
    global blink, ena
    if ena:
        print("Can't change time when alarm!")
        return
    t = time.ticks_ms()
    if t < preirq[0] + 10:
        return
    preirq[0] = t
    blink += 1
    blink %= 7
    return

def Add_b(p):
    global delta, blink, ena
    if ena:
        print("Can't change time when alarm!")
        return
    t = time.ticks_ms()
    if not blink or t < preirq[1] + 10:
        return
    preirq[1] = t
    delta += 1
    return

def Minus_c(p):
    global delta, blink, ena
    if ena:
        print("Can't change time when alarm!")
        return
    t = time.ticks_ms()
    if not blink or t < preirq[2] + 10:
        return
    preirq[2] = t
    delta -= 1
    return

a = button(0,Select_a)
b = button(14,Add_b)
c = button(2,Minus_c)
piezo = PWM(Pin(12, Pin.OUT), freq=Alerm_Frequency, duty=1024)
adc = ADC(0)
rtc = RTC()
rtc.datetime(Init_Time)  # set a specific date and time
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
buf = bytearray(10)  # create a buffer with 10 bytes
i2c.writeto(0x3C, buf)  # write the given buffer to the peripheral
display = ssd1306.SSD1306_I2C(128, 32, i2c)

global delta, blink, ena
delta, blink = 0, 0
preirq = [-10, -10, -10]  # for [a,b,c]
k = Blink_Interval_ms // (85.71)
mx = 0  # adaptive
for i in range(1000):
    mx = max(mx, adc.read())
for cnt in range(10**9):
    t = time.ticks_ms()
    Year, Month, Day, Week, Hour, Min, Sec, Msec = rtc.datetime()
    ena = (
        1
        if not blink and Hour == Hour_Set and Min == Minute_Set and Sec < Alarm_Time
        else 0
    )
    if ena and not blink:
        piezo.duty(1024 if cnt // k % 2 else Alerm_Duty)
    if not ena:
        piezo.duty(1024)
    
    if blink:
        if blink == 1:
            Hour += delta
            Hour %= 24
        elif blink == 2:
            Min += delta
            Min %= 60
        elif blink == 3 and Msec < 100:
            Sec += delta
            Min %= 60
            delta = 0
        elif blink == 4:
            Year += delta
        elif blink == 5:
            x = Month-1
            x += delta
            x %= 12
            Month = x+1
        elif blink == 6:
            x = Day-1
            x += delta
            x %= M1[Month] if Year % 4 or (not Year % 100 and Year % 1000) else M2[Month]
            Day = x+1
        if blink != 3:delta = 0
        rtc.datetime((Year, Month, Day, Week, Hour, Min, Sec, Msec))
    show(Hour, Min, Sec, k, cnt, blink, ena)
