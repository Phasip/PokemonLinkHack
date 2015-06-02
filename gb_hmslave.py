import time,binascii,sys
from modules import gb_link_trader,pkmn_pokedata

if len(sys.argv) > 1:
    gb_link_trader.init(sys.argv[1])
else:
    gb_link_trader.init('no')

name = "Pasi" # Name of player
pokemon_name = "Mew"
outPokemon = pkmn_pokedata.hmslave #Seems like some data is ignored, such as pokemon type
gb_link_trader.sendMon(name,name,pokemon_name,outPokemon)
gb_link_trader.abortTrade()
