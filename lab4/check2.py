from machine import *
import time
import ssd1306

spi = SPI(1, baudrate=1500000, polarity=1, phase=1)
cs = Pin(15, Pin.OUT)
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
buf = bytearray(10)  # create a buffer with 10 bytes
i2c.writeto(0x3C, buf)  # write the given buffer to the peripheral
display = ssd1306.SSD1306_I2C(128, 32, i2c)

SPI_READ = 1 << 7
SPI_WRITE = 0 << 7

SPI_SINGLE_BYTE = 0 << 6
SPI_MUTIPLE_BYTES = 1 << 6

cs.value(0)
spi.write(bytes([0x31, 0x0C]))
cs.value(1)
cs.value(0)
spi.write(bytes([0x2D, 0x28]))
cs.value(1)
cs.value(0)
spi.write(bytes([0x2C, 0x0A]))
cs.value(1)
cs.value(0)
spi.write(bytes([0x2E, 0x00]))
cs.value(1)
cs.value(0)
spi.write(bytes([0x38, 0x00]))
cs.value(1)

read_buffer = bytearray(7)
ID_REG = 0x32

def get_data():
    cs.value(0)
    spi.readinto(read_buffer, SPI_READ | SPI_MUTIPLE_BYTES | ID_REG)
    cs.value(1)
    x, y, z = (
        read_buffer[2] << 8 | read_buffer[1],
        read_buffer[4] << 8 | read_buffer[3],
        read_buffer[6] << 8 | read_buffer[5],
    )
    if x > 32767:
        x -= 65536
    if y > 32767:
        y -= 65536
    if z > 32767:
        z -= 65536
    return x,y,z

def show(x,y):
    display.fill(0)
    display.text('test', x, y, 1)
    display.show()

x,y = 0,0
while 1:
    show(x,y)
    acx,acy,_ = get_data()
    Acx,Acy = abs(acx),abs(acy)
    if Acx > 8000:
        dx = acx//1000 - 7
        sign = 1 if acx > 0 else -1
        x += sign * dx
    if Acy > 8000:
        dy = acy//1000 - 7
        sign = 1 if acy > 0 else -1
        y += sign * dy

