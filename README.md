PokemonLinkHack
===========================

## Pins
Note that, to ensure that you don't break your Raspberry Pi, a 10kOhm resistor
is recommended at the MISO pin (GB uses 5v output)
Note that you should always use the Rpi as master, otherwise you may want to
add a 10kOhm resistor to SCLK too (Always run script before talking to pokecenter lady).
(I have been using this without any resistors, and my raspi isn't broken yet...)

     ___________
    |  6  4  2  |
     \_5__3__1_/   (at cable)

    Cable Pin   Name           Raspberry GPIO         BusPirate Pins
       1        VCC                N/A                    N/A
       2        Serial Out         BCM 10 (MISO)          MISO
       3        Serial In          BCM 9 (MOSI)           MOSI
       4        Serial Data        N/A                    N/A
       5        Serial Clock       BCM 11(SCLK)           CLK
       6        GND                Ground                 GND
       
       
## Stuff
Abuse the link cable to transfer and execute code in your pokemon blue/red(/yellow?) on gameboy classic.
This is a bit unstable - you may need to restart your device to get a transfer working.
Note that the code is made for python3

## Backends
All scripts take a single argument. This argument specifies which backend to use

'pi' = Raspberry Pi SPI port

'bp' = Buspirate SPI

'no' = BGB emulator link
## gb_hmslave.py 
Simply trade a hm-slave Mew to your gameboy.
## gb_install_programs.py
Uses the exploit described by [vaguilar](http://vaguilar.js.org/posts/1/) to add program pokemons
to your current box. Your box must be empty, you need to have less than 20 items 
and the trainer name of any pokemon in daycare will be changed.
This gives you the 0x7A item (Name is weird characters) which 
allows you to run "program pokemons" that are installed in your boxes.

After the exploit has run, abort the trade and walk around til your pokemons die.
Then save the game by changing box.
## getbytes.py
Compiles a .asm file and tries to extract the relevant bytes from the result.
These bytes can be used with modules/gbexploit.py or gb_install_programs.py
Uses symbol files that are generated when compiling [pokered](https://github.com/iimarckus/pokered).
(you need to modify ASMLOC to match your location of pokered)
## modules/
Parts that can be used to do stuff with pokemon/gameboy/spi
## programs/
Assembly code of some programs that can be used with this stuff.
Programs include red/main.asm to get access to non-global labels.
Programs must start with the byte sequence "START" and end with the byte
sequence "END" to make extraction with getbytes.py simple.

## 7A item
The 7A item is a item similar to [8F](http://forums.glitchcity.info/index.php/topic,6638.0.html), except execution starts inside
the original trainer name of the current daycare pokemon. (DA58).
gb_install_program uses the OT name to jump to the first box pokemon - which 
is made to contain code that lists the boxed pokemons and execute code that they
contain.
