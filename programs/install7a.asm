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
    push hl
    ld hl,wNumBagItems ;First item
    ld (hl),7a ;Set to 7a
    inc hl
    ld (hl),99
    ld hl,W_DAYCAREMONOT+4
    ld (hl),18 ; Relative jump
    inc hl
    ld (hl),wBoxMon1-(W_DAYCAREMONOT+4) ; To DA9a
    pop hl
    ret
ENDLABL::
    db $45
    db $4e
    db $44
