import time,binascii,sys
from modules import pkmn_chars,pkmn_pokedata

def init(backend):
    if sys.version_info<(3,0,0):
        print("WARNING: You are using python2!")
        print("WARNING: The code is written with python3 in mind, use carefully with python2")
        
    global sendDataByte
    if backend == "no":
        from modules import bgb_master
        print("Initializing emulator stuff...")
        bgb_master.init()
        time.sleep(1)
        sendDataByte = bgb_master.sendDataByte
    elif backend == "bp":
        from modules import buspirate
        sendDataByte = buspirate.sendDataByte
        print("Running with buspirate backend")
        buspirate.bus_init()
    elif backend == "pi":
        from modules import raspberry
        sendDataByte = raspberry.sendDataByte
        print("Running with raspberry pi backend")
        raspberry.bus_init()
    else:
        print("Unknown backend, pi = raspberry pi, bp = buspirate, no = bgb emulator")
        sys.exit(0)
    


def sendGb(data,wait = 0.005,resend = True, echo=True):
    ret = b''
    for i in data:
        val = sendDataByte(i)
        time.sleep(wait)
        while val == 0xFE and resend == True:
            val = sendDataByte(i)
            time.sleep(wait)
        ret = ret + bytes((val,))
    
    if echo:
        print("Sent: " + str(binascii.hexlify(data)))
        print("Recv: " + str(binascii.hexlify(ret)))
    
    return ret

def sendUntil(data,waitfor,wait = 0.02):
    retval = None
    print("Sending: %s, until: %s"%(str(binascii.hexlify(data)),str(binascii.hexlify(waitfor))))
    print("Recv: [",end="")
    while retval != waitfor:
        retval = sendGb(data,wait,echo=False)
        print("%s,"%str(binascii.hexlify(retval)),end="")
    print("], Done!")
    return retval

def sendUntilrecvdSequence(send,waitfor):
    received = b''
    while True:
        if waitfor == received:
            return
        received = received + sendGb(send)
        received = received[-len(waitfor):]
        
        
def sync(byte = b"\x60"):
    sendGb(b"\x60"*13)
    sendGb(b"\x00"*10)

def wait_60(byte=b"\x60"):
    retval = 0x70
    while (retval >> 4) != 6:
        retval = sendGb(byte,0.2)[0]
        
    return bytes((retval,))
    
    sendUntil(b"\x60",b"\x60")

