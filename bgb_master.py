import socket,sys,timeit,threading,time,binascii,errno
from ctypes import c_uint32

#Connect to BGB and act as master when communicating.
#Adapted for pokemon - replies 01 if BGB tries to act as master.


SLEEP_TIME=0.001
HANDSHAKE_DATA = b"\x01\x01\x04\x00\x00\x00\x00\x00"
class Client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1",8765))
        s.setblocking(0)
        self.buff = b''
        self.s = s
        self.data_out = None
        self.data_in = None
        self.paused = False
        self.handshake = 0
        
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
        (b1,b2,b3,b4) = data[0:4]
        i1 = data[4:8]
        
        if b1 == 1: # Version
            self.send(HANDSHAKE_DATA)
            return
        if b1 == 101: # Joypad
            self.send(data)
            return
        if b1 == 104: # Sync1
            self.send(bytes((106,0,0,0,)) + self.t())
            #We are always master, ignore all sync1
            if b3 == 0x81:
                #POKEMON HACK, REPLY 1 IF DATA REQUEST
                self.send(bytes((105,1,0x80,0))+b'\x00\x00\x00\x00')
            return
        if b1 == 105: #Sync2
            self.send(bytes((106,0,0,0,)) + self.t())
            if self.data_in == None:
                self.data_in = b2
            return
        if b1 == 106: # Sync3
            #if b2 == 0: #Synchronization message
            self.send(bytes((106,0,0,0,)) + self.t())
            return
        if b1 == 108:
            self.send(bytes((108,1,0,0,0,0,0,0)))
            return
    
    def run(self):
        print("Client started!")
        running = 1
        while running:
            if self.data_out != None:
                self.send(bytes((104,self.data_out,0x81,0,))+self.t())
                self.send(bytes((106,0,0,0,)) + self.t())
                self.data_out = None
            try:
                msg = self.s.recv(4096)
                
            except socket.error as e:
                if e.args[0] == errno.EWOULDBLOCK:
                    time.sleep(SLEEP_TIME)
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
                    
    def write_gb(self,byte):
        while self.data_out != None: #This should never happen
            time.sleep(SLEEP_TIME)
        self.data_in = None
        self.data_out = byte
        while self.data_out != None:
            time.sleep(SLEEP_TIME)
        while self.data_in == None:
            time.sleep(SLEEP_TIME)
        return self.data_in
        

def init():
    global c
    c = Client()
    c.start()

def sendDataByte(byte):
    global c
    return c.write_gb(byte)
