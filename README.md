# PokemonLinkHack
Abuse the link cable to transfer and execute code in your pokemon blue/red(/yellow?) on gameboy classic.

(Sorry for the state of everything, contact me for any and all questions - thought it would be better to put it on github than leaving it offline)

Some tools I used to connect my computer & pokemon on gameboy color.

All tools take a single argument "bp" or "no" - bp = connect through buspirate, no = use bgb emulator link

Helps creating the 8F code execution item and use the link cable to transfer code to execute.

Can create 8F if you have an old rod/good rod and a couple of worthless pokemons.

With the 8F we can execute code located in our pokemon, tentacool with serial recv and execute code included.

(Attempt to create F8 by overwriting the box-pokemon counter - has some issues with stack overflows - 
think it would work by depositing 8 pokemons before trading)

Used buspirate to communicate, a raspberry pi could probably be used if 
a voltage drop for gameboy output pin is added.

Link cable http://www.hardwarebook.info/Game_Boy_Link
Buspirate linking
SI - MOSI
SO - MISO
CLK - SC
GND -GND
Gameboy can act as Master/Slave (Master sends clock signals)




Thanks to:
Disassembly of Pokémon red: https://github.com/iimarckus/pokered

Arbitrary code execution with 8F item: http://forums.glitchcity.info/index.php/topic,6638.0.html
