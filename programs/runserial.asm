INCLUDE "red/main.asm"
SECTION "Nobank",ROMX,BANK[$ff]
;PokeLok EQU $D89c
;Serial_Exchange_Bytes EQU $216f
STARTLABL::
    db $53
    db $54
    db $41
    db $52
    db $54
SomeLabel::
    ld hl,wEnemyPartyCount
    ld de,wEnemyPartyCount
    ld bc, $01A8
    call Serial_ExchangeBytes ;call stuff
    ld hl, wEnemyPartyCount+20
    jp hl
ENDLABL::
    db $45
    db $4e
    db $44
