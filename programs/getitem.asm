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
    xor a
    dec a
    ld hl,wcf97 ;Max quantity
    ld [hl],a
    call DisplayChooseQuantityMenu
    ld hl,wcf96 ;Selected quantity
    ld a,[hl]
    ld [wcf91],a ;Item to add
    ld a,63 ;Quantity to add
    ld [hl],a
    ld hl,wNumBagItems
    jp AddItemToInventory
ENDLABL::
    db $45
    db $4e
    db $44
