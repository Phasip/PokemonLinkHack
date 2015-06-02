#!/usr/bin/python
# Requires gbasm and rgblink to be installed
# Requires pokered code to be compiled and compilation files not removed
# Change ASMLOC to match your location of the compiled files

# Takes a asm file, compiles it and outputs the bytes between START and END
# Symbols from text.o, wram.o and audio.o are available directly, asm 
#  file should include main.o to get access to non-global labels

# Note, only tested on linux - not made with compability in mind

import sys,tempfile,binascii,os
from subprocess import call
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
        

ASMLOC = "~/pokered/"
start = b"START"
end = b"END"    

asm = os.path.abspath(sys.argv[1])

with cd(ASMLOC):
    if len(sys.argv) != 2:
        print("Use file.asm as argument")
        sys.exit(-1)

    
    fil = tempfile.NamedTemporaryFile()
    retcode = call(["rgbasm","-h","-o",fil.name,asm])
    if retcode != 0:
        fil.close()
        print("Failed to build!")
        sys.exit(-1)

    fil2 = tempfile.NamedTemporaryFile()
    #I hope our assembly don't mess with addresses...?
    ret2 = call(["rgblink","-o",fil2.name,"red/text.o","red/wram.o","red/audio.o",fil.name])
    data = fil2.read()
    fil.close()
    fil2.close()
    if ret2 != 0:
        print("Failed to link!")
        sys.exit(-1)

    if len(data) == 0:
        print("Output seems empty?")
        sys.exit(-1)
        
    startloc = data.find(start)
    endloc = data.find(end)
    if startloc == -1 or endloc == -1:
        print("Could not find start (%s) or end (%s)"%(start,end))
        sys.exit(-1)
        
    if data.find(start,startloc+1) != -1 or  data.find(end,endloc+1) != -1:
        print("Start or end code exists multiple times in file... Change start and end code")
        sys.exit(-1)
    code = data[startloc+len(start):endloc]
    hexdata = binascii.hexlify(code).decode('ascii')
    if b"\xFE" in code:
        print("Warning: Code contains byte 0xFE, may cause problems with serial transfer")
    print("Code: %s"%hexdata)
    print("Len: %d bytes"%len(code))
