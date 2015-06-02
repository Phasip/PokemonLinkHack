#!/usr/bin/python3
import spidev



# https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/
# add spi-bcm2708 to /etc/modules
# add dtparam=spi=on to your /boot/config.txt (reboot)
# sudo apt-get install python3 python3-dev git
# git clone https://github.com/doceme/py-spidev.git
# cd py-spidev
# sudo python3 setup.py install


def bus_init():
    global spi
    spi = spidev.SpiDev()
    spi.open(0,0)

def sendDataByte(byte):
    global spi
    return spi.xfer([byte])[0]
