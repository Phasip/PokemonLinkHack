#!/usr/bin/python
hex_to_char = {0x4F: "=",
0x57: "#",
0x51: "*",
0x52: "A1",
0x53: "A2",
0x54: "PK",
0x55: "+",
0x58: "$",
0x7F: " ",
0x80: "A",
0x81: "B",
0x82: "C",
0x83: "D",
0x84: "E",
0x85: "F",
0x86: "G",
0x87: "H",
0x88: "I",
0x89: "J",
0x8A: "K",
0x8B: "L",
0x8C: "M",
0x8D: "N",
0x8E: "O",
0x8F: "P",
0x90: "Q",
0x91: "R",
0x92: "S",
0x93: "T",
0x94: "U",
0x95: "V",
0x96: "W",
0x97: "X",
0x98: "Y",
0x99: "Z",
0x9C: ":",
0xA0: "a",
0xA1: "b",
0xA2: "c",
0xA3: "d",
0xA4: "e",
0xA5: "f",
0xA6: "g",
0xA7: "h",
0xA8: "i",
0xA9: "j",
0xAA: "k",
0xAB: "l",
0xAC: "m",
0xAD: "n",
0xAE: "o",
0xAF: "p",
0xB0: "q",
0xB1: "r",
0xB2: "s",
0xB3: "t",
0xB4: "u",
0xB5: "v",
0xB6: "w",
0xB7: "x",
0xB8: "y",
0xB9: "z",
0xBA: "‚",
0xBC: "'l",
0xBD: "'s",
0xBE: "'t",
0xBF: "'v",
0xE0: "'",
0xE1: "PK",
0xE2: "MN",
0xE3: "-",
0xE4: "'r",
0xE5: "'m",
0xE6: "?",
0xE7: "!",
0xE8: ".",
0xF4: ",",
0xF6: "0",
0xF7: "1",
0xF8: "2",
0xF9: "3",
0xFA: "4",
0xFB: "5",
0xFC: "6",
0xFD: "7",
0xFE: "8",
0xFF: "9"}
char_to_hex = dict([v,k] for k,v in hex_to_char.items())
def sendString(text,length):
    ret = b""
    if len(text) >= length:
        print("Text too long!")
        sys.exit(1)
        
    for i in text:
        if not (i in pkmn_chars.char_to_hex):
            print("Illegal pokemon char: " + i)
            sys.exit(1)
        
        ret = ret +  bytes((pkmn_chars.char_to_hex[i],))
    ret = ret + b"\x50"*(length-len(ret)) #String end and fill
    return ret

def string_to_gb(text):
    global char_to_hex
    ret = b""
    for i in text:
        if not (i in char_to_hex):
            print("Illegal pokemon char: " + i)
            sys.exit(1)
        ret = ret + bytes((char_to_hex[i],))
    return ret
              
def gb_to_string(data):
    global hex_to_char
    ret = ""
    for i in data:
        if not (i in hex_to_char):
            ret = ret + "."
        else:
            ret = ret + hex_to_char[i]
    return ret
