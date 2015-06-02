INCLUDE "red/main.asm"
SECTION "Nobank",ROMX,BANK[$ff]
;PLACECODE EQU $DEF0
STARTLABL::
    db $53
    db $54
    db $41
    db $52
    db $54
MyCode::
    ld c,$26
    ld hl,wPokedexOwned
    ld a,$ff
.loop
    ldi [hl],a
    dec c
    jr nz,.loop
    dec hl
    ld [hl],$7f ;End of wPokedexSeen
    ld hl,wPokedexSeen-1
    ld [hl],$7f
    ret
ENDLABL::
    db $45
    db $4e
    db $44
    
    


