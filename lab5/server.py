from machine import *
import ssd1306
import network
import time
import urequests
import socket

button = Pin(2,Pin.IN)
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
display = ssd1306.SSD1306_I2C(128, 32, i2c)

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('SpectrumSetup-77', 'jollydesk715')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def show():
    display.fill(0)
    display.fill_rect(0, 0, 32, 32, 1)
    display.fill_rect(2, 2, 28, 28, 0)
    display.vline(9, 8, 22, 1)
    display.vline(16, 2, 22, 1)
    display.vline(23, 8, 22, 1)
    display.fill_rect(26, 24, 2, 4, 1)
    display.text('MicroPython', 40, 0, 1)
    display.text('SSD1306', 40, 12, 1)
    display.text('OLED 128x64', 40, 24, 1)
    display.show()
    return

def showtime():
    display.fill(0)
    url = 'http://worldclockapi.com/api/json/est/now'
    re = urequests.get(url)
    re = re.json()
    T = re['currentDateTime']
    Hour = T[11:13];Min = T[14:16]
    color = 1
    display.rect(61, 18, 2, 2, color)
    display.rect(61, 21, 2, 2, color)
    display.text(Hour, 44, 17, color)
    display.text(Min, 64, 17, color)
    display.show()
    display.show()

do_connect()

addr = ('192.168.1.70',9999)
s = socket.socket()
s.bind(addr)
s.listen(100)

while True:
    try:
        (conn,address) = s.accept()
    except OSError:
        # print("Nothing")
        pass
    else:
        rec = conn.recv(4096)
        rec = rec.split(b'\r\n\r\n')
        rec = str(rec[0])
        rec = rec[2:-1]
        if 'on' in rec:show()
        elif 'off' in rec:
            display.fill(0)
            display.show()
        elif 'time' in rec:showtime()
        else:
            display.text(rec, 44, 10, 1)
    time.sleep(0.01)
