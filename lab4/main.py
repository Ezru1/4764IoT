from machine import *
import time

spi = SPI(1, baudrate=1500000, polarity=1, phase=1)
cs = Pin(15, Pin.OUT)

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
while 1:
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
    print(x, y, z)
    time.sleep(0.5)
