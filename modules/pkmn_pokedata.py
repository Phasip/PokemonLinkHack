#!/usr/bin/python
from collections import namedtuple
from struct import unpack,pack

#D16B - Pokémon (Again) 
#D16C-D16D - Current HP 
#D16E - Level 
#D16F - Status (Poisoned, Paralyzed, etc.) 
#D170 - Type 1 
#D171 - Type 2 
#D172 - Catch rate/Held item (When traded to Generation II) 
#D173 - Move 1 
#D174 - Move 2 
#D175 - Move 3 
#D176 - Move 4 
#D177-D178 - Trainer ID 
#D179-D17B - Experience 
#D17C-D17D - HP EV 
#D17E-D17F - Attack EV 
#D180-D181 - Defense EV 
#D182-D183 - Speed EV 
#D184-D185 - Special EV 
#D186 - Attack/Defense IV 
#D187 - Speed/Special IV 
#D188 - PP Move 1 
#D189 - PP Move 2 
#D18A - PP Move 3 
#D18B - PP Move 4 
#D18C - Level 
#D18D-D18E - Max HP 
#D18F-D190 - Attack 
#D191-D192 - Defense 
#D193-D194 - Speed 
#D195-D196 - Special 
    

data = b"\xB0\x00\x15\x00\x00\x14\x14\x2D\x0A\x2D\x00\x00\x46\xFA\x00\x00\xDD\x00\x4A\x00\x68\x00\x64\x00\x73\x00\x4B\x5A\xF2\x23\x28\x00\x00\x06\x00\x15\x03\x0B\x00\x0B\x00\x0E\x00\x0B"
pkmn_format = ">B H 9B H 3s 5H 7B 5H"
Pokemon = namedtuple('Pokemon', 'Pokemon Current_HP Level_1 Status Type1 Type2 Catch_rate Move_1 Move_2 Move_3 Move_4 Trainer_ID Experience HP_EV Attack_EV Defense_EV Speed_EV Special_EV AttackDefense_IV SpeedSpecial_IV PP_Move_1 PP_Move_2 PP_Move_3 PP_Move_4 Level_2 Max_HP Attack Defense Speed Special')
charamander = Pokemon._make(unpack(pkmn_format,data))
hmslave = charamander._replace(Pokemon=0x15, #Mew
Move_1 = 0x0F, #Cut
Move_2 = 0x13, #Fly
Move_3 = 0x39, #Surf
Move_4 = 0x46, #Strength
Level_2 = 45,
Max_HP=255,
Defense=779)

def make_pkmn(data):
    if len(data) == 33:
        data = data + b"\x00"*11
    return Pokemon._make(unpack(pkmn_format,data))

#Replace some bytes in a pokemon byte representation
def modify_pkmn_bytes(pokemon,index,data):
    global pkmn_format,Pokemon
    orig = pack(pkmn_format,*pokemon)
    new = orig[0:index] + data + orig[index+len(data):]
    return Pokemon._make(unpack(pkmn_format,new))
    
#Get byte representation of pokemon
def get_pkmn_bytes(pokemon):
    global pkmn_format
    return pack(pkmn_format,*pokemon)
