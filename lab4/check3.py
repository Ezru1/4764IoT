from machine import *
import ssd1306
import network
import time
import urequests
import ujson
import os 
button = Pin(2,Pin.IN)
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
buf = bytearray(10)  # create a buffer with 10 bytes
i2c.writeto(0x3C, buf)  # write the given buffer to the peripheral
display = ssd1306.SSD1306_I2C(128, 32, i2c)
wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
wlan.scan()             # scan for access points
wlan.isconnected()      # check if the station is connected to an AP
ssid = 'Columbia University'

wlan.connect(ssid) # connect to an AP
wlan.config('mac')      # get the interface's MAC address
wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses

ap = network.WLAN(network.AP_IF) # create access-point interface
ap.active(True)         # activate the interface
ap.config(ssid='ESP-AP') # set the SSID of the access point

def show(x,y,s):
    display.text(s, x, y, 1)
    display.show()

url0 = 'http://ip-api.com/json'
r = urequests.get(url0)
r = r.json()
latitude = r['lat']
longtitude = r['lon']
print(r)
while 1:

    time.sleep(1)
    if not button.value():
        url = 'http://api.weatherapi.com/v1/current.json?'
        url += 'key=713bc638bd8842a695855217230610'
        url += '&q=%s,%s'%(latitude,longtitude)
        url += '&api=no'
        re = urequests.get(url)
        re = re.json()
        print(re)
        Weather_type = re['current']['condition']['text']
        Weather_temp = re['current']['temp_f']
        display.fill(0)
        show(0,0,str(latitude)[:-2])
        show(50,0,str(longtitude)[:-2])
        show(0,10,Weather_type)
        show(0,20,str(Weather_temp))
        urequests.post("http://ntfy.sh/Zzz",data="Latitude:%s Longtitude:%s\nWeather:%s Temperature:%s"%(latitude,longtitude,Weather_type,Weather_temp))