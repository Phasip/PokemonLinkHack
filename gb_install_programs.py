import time,binascii,sys
from modules.gblink import sendGb,sendUntil,wait_60
from modules.gbexploit import init,exploit
from modules import pkmn_chars
#Pre-req: Voltrob & SerialRecv tentacool, f8
#Result: Run code - fill pokedex up to 152 pokemons.


if len(sys.argv) == 1:
    init('no')
else:
    init(sys.argv[1])
    
b = b'21e9cee5e5d1010400cd6f21e12af52af52af52a4ff16ff167f13d280f3d2801c92ae0accd9a210d20f718d4e5d10600cd6f2118cb' #serialcomm.asm
bytecode =  binascii.unhexlify(b)


def writedata(addr,data):
    sendGb(b"\x00"*20) #Just some buffer
    sendGb(b"\xFD") #Okay, lets go!
    sendGb(b"\x01")
    sendGb(addr.to_bytes(2,byteorder='big'))
    sendGb((len(data)).to_bytes(1,byteorder='big'))
    sendGb(b"\x00"*20) #Just some buffer
    sendGb(b"\xFD") #Okay, lets go!
    sendGb(data)
    
def readdata(addr,length):
    sendGb(b"\x00"*20) #Just some buffer
    sendGb(b"\xFD") #Okay, lets go!
    sendGb(b"\x02")
    sendGb(addr.to_bytes(2,byteorder='big'))
    sendGb((length+1).to_bytes(1,byteorder='big'))
    return sendGb(b"\x00"*(length+1))[1:]

def runfinish():
    sendGb(b"\x00"*20) #Just some buffer
    sendGb(b"\xFD") #Okay, lets go!
    sendGb(b"\x03"*4)
    

def addBoxData(trainer,name,data):
    mons = ord(readdata(0xda80,1))
    monid = data[0:1]
    print("Mons: %i"%mons)
    print("Monid: %s"%binascii.hexlify(monid))
    writedata(0xda80,bytes((mons+1,)))
    writedata(0xda80+1+mons,monid +b'\xff')
    writedata(0xda96+mons*0x21,data)
    writedata(0xdd2a+mons*11,pkmn_chars.string_to_gb(trainer,11))
    writedata(0xde06+mons*11,pkmn_chars.string_to_gb(name,11))

def poisonMons():
    mons = ord(readdata(0xd163,1))
    for i in range(mons):
        writedata(0xd16c+0x2c*i,bytes((0,1,)))
        writedata(0xd16f+0x2c*i,bytes((8,)))
        
def addItem(code,num=99,force=False):
    items = ord(readdata(0xD31D,1))
    if items >= 20 and force == False:
        sys.exit("Too many items!")
        return
    writedata(0xd31d,bytes((items+1,)))
    writedata(0xd31e+2*items,bytes((code,num,0xff)))

exploit(bytecode)
writedata(0xda58,b'\x18\x3d\x50')
addBoxData('HAX','7ARunner',binascii.unhexlify(b'18003e08cdbc352180dacdbe56cdcd353001c92197dafa92cf012100cd873ae9'))
addBoxData('HAX','RunSerial',binascii.unhexlify(b'180000002193D81193D801A801CD6F2121A8D8E900000000000000000000000000'))
addBoxData('HAX','GetItem',binascii.unhexlify(b'18000000AF3D2197CF77CD572D2196CF7EEA91CF3E6377211DD3C3CF2B00000000'))
addBoxData('HAX','FillDex',binascii.unhexlify(b'180000000E2621F7D23EFF220D20FC2B367F2109D3367FC9000000000000000000'))
# writedata(0xd12b,b'\x00') # set wLinkState to 0 in order to use items ... Does not work for some reason..
addItem(0x7A,1)
# Poison the Pokémons so we can exit and save through the box!
poisonMons()
#Don't do this... saves you in the center and you can't leave.
#b = readdata(0xd72e,1) 
#writedata(0xd72e,bytes((b[0]&~(1<<6),))) # set bit 6 of wd72e to 0 to save

runfinish()

#Exploit code finished, abort trade!
wait_60(b"\x6f") #Abort trade
sys.exit(0)
