import socket,sys,timeit,threading,time,binascii,errno
from ctypes import c_uint32
import buspirate

#Link BGB and gameboy connected through buspirate - adapted for pokemon

HANDSHAKE_DATA = b"\x01\x01\x04\x00\x00\x00\x00\x00"
buspirate.bus_init()
init = True
def get_reply(byte):
    global init
    time.sleep(0.01)
    ret = buspirate.sendDataByte(byte)
    if not init:
        return ret
    if ret == 1:
        ret = 0
    init = False
    return ret
    
lastData = None
class Client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1",8765))
        s.setblocking(0)
        self.buff = b''
        self.s = s
        self.send(HANDSHAKE_DATA)
        
    def t(self):
        timestamp = int(timeit.default_timer()*(2**21)) & 0x7FFFFFFF
        l = c_uint32(timestamp)
        return bytes(l)
        
    def send(self,data):
        #Todo, read current blocking and reset
        self.s.setblocking(1)
        self.s.send(data)
        self.s.setblocking(0)
        
    def msg(self,data):
        global lastData
        (b1,b2,b3,b4) = data[0:4]
        i1 = data[4:8]
        
        if b1 == 1: # Version
            self.send(HANDSHAKE_DATA)
            return
        if b1 == 101: # Joypad
            self.send(data)
            return
        if b1 == 104: # Sync1
            if lastData == data: #Do not handle resent messages.
                return
            lastData = data
            if b3 == 0x81:
                #We are the slave, only reply to master
                self.send(bytes((105,get_reply(b2),0x80,0))+b'\x00\x00\x00\x00')
                
            return
        if b1 == 105: #Sync2
            #self.send(bytes((106,0,0,0,)) + self.t())
            return
        if b1 == 106: # Sync3
            if b2 == 0: #Synchronization message
                self.send(bytes((106,0,0,0,)) + self.t())
            return
        if b1 == 108:
            self.send(data)
            return
    
    def run(self):
        print("Client started!")
        while True:
            try:
                msg = self.s.recv(4096)
                
            except socket.error as e:
                if e.args[0] == errno.EWOULDBLOCK:
                    #self.send(bytes((106,0,0,0,)) + self.t())
                    time.sleep(0.001)
                    continue
                else:
                    print(e)
                    sys.exit(1)
            else:
                if not msg:
                    print("Conn closed")
                    self.s.close()
                    break
                self.buff = self.buff+msg
                while len(self.buff) >= 8:
                    self.msg(self.buff[0:8])
                    self.buff = self.buff[8:]        
            
c = Client()
c.start()
