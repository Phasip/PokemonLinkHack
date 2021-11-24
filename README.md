PokemonLinkHack
===========================
This repo is a bunch of tools used to abuse the link-cable buffer overflow vulnerability in the
Pokemon Red (Gen1). The main script to use is gb_install_programs which first exploits the vulnerability to run code that allows us to read and write arbitrary memory addresses over the link cable. This is then used to add the 0x7A item to the players inventory. "Use" on 0x7A executes data within the Original-Trainer Name of the current pokemon in daycare. We overwrite this with code that jumps to the data stored in the first pokemon storage box.
Instead of placing a real pokemon in the storage box, we place a program which lists other programs in subsequent boxes, and allows the user to run these.

Finally, to be able to save the state the script poisons all your pokemons. You walk around till all your mons die, then go to the box storage system and change box in order to save.

Now you can reset your game, load the save and use the 0x7a item!
## Images
![Prepping](/images/1.png)  
*Prepping*

![Start Trade](/images/2.png)  
*Start trade*

![Trading, just cancel](/images/3.png)  
*Trading, just cancel*  

![Die by walking around](/images/4.png)  
*Die by walking around*

![Save by changing box](/images/5.png)  
*Save by changing box*

![Save by changing box, then reset the game](/images/6.png)  
*Save by changing box, then reset the game*

![Use item 0x7A](/images/7.png)  
*Use item 0x7a*

![Use program FillDex](/images/8.png)  
*Use program FillDex*

![Pokedex has been filled](/images/9.png)  
*Pokedex has been filled*

![Looking at stored mons in boxes](/images/10.png)  
*Looking at stored mons in boxes*

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
Uses the exploit described by [vaguilar](http://web.archive.org/web/20180508011842/http://vaguilar.js.org/posts/1/) to add program pokemons
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
