#!/usr/bin/python
import sys,time,serial,binascii
#Raw 3wire mode for buspirate
bp = None
def sendByte(byte,verify=False):
    bp.write(bytes((byte,)))
    if verify:
        r = bp.read(1)
        if r == b"\x01":
            return
        sys.exit('Fails: ' + str(r))

def sendDataByte(byte):
    bp.write((0b00010000,byte,))
    return bp.read(2)[1]
    
def sendData(data,wait = 0):
    ret = b''
    bp.timeout = 2.0
    for i in data:
        ret += bytes((sendDataByte(i),))
        time.sleep(wait)
    
    print("Sent: " + str(binascii.hexlify(data)))
    print("Recv: " + str(binascii.hexlify(ret)))
    bp.timeout = 0.1
    return ret


def sendUntil(send,recv):
    ret =""
    while ret != recv:
        ret = sendData(send)
        time.sleep(0.5)
    
def bus_init():
    global bp
    bp = serial.Serial("/dev/ttyUSB0", 115200,timeout=0.1)
    for i in range(25):
        sendByte(0b00000000)
        ret= bp.read(5)
        if ret == b"BBIO1":
            break
    else:
        print("Fail to init!")
        sys.exit(-1)

    print("In Binary Mode!")
    sendByte(0b00000101) # 0b00000101 Enter binary raw-wire mode, responds "RAW1"
    ret = bp.read(4)
    if ret != b"RAW1":
        print("Did not enter raw mode, exit")
        sys.exit(-1)
    print("Setting speed")
    sendByte(0b01100000,True)  #011000xx – Set speed, 3=~400kHz, 2=~100kHz, 1=~50kHz, 0=~5kHz
    print("Setting 3wire mode")
    sendByte(0b10001100,True) #1000wxyz – Config, w=HiZ/3.3v, x=2/3wire, y=msb/lsb, z=not used
    print("In Raw mode!")
