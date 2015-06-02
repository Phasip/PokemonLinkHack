INCLUDE "red/main.asm"
SECTION "Nobank",ROMX,BANK[$ff]
;Restarts game but gives the player the items 0x5D (8F) and 0xFA (??)
PLACECODE EQU $DEF0
STARTLABL::
    db $53
    db $54
    db $41
    db $52
    db $54
MyCode:: 
.init
    ld hl,wBuffer
    push hl
    push hl
    pop de
    ld bc,4
    call Serial_ExchangeBytes ;call stuff
    pop hl
    ld a,[hli]
    push af;What to do
    ld a,[hli]
    push af;Where to do it (high)
    ld a,[hli]
    push af;Where to do it (low)
    ld a,[hli] ; How many bytes
    ld c,a ; c = number of bytes
    pop af
    ld l,a
    pop af
    ld h,a; hl = where
    pop af; a = what
    dec a
    jr z,.writeloop ; if a=1 writeloop
    dec a
    jr z,.readloop ; if a=2 readloop
    ret ;Exit if we received some other message
.readloop
    ld a,[hli]
    ld [hSerialSendData], a
    call Serial_ExchangeByte
    dec c
    jr nz,.readloop
    jr .init
.writeloop
    push hl
    pop de
    ld b,0
    call Serial_ExchangeBytes
    jr .init
.codeend
    ;Here we can put additional code received by serial
ENDLABL::
    db $45
    db $4e
    db $44
    

GetSP::
    ;Becomes: cd5914e8fee1 (6 bytes)
    call HandlePartyMenuInput-1
.hlpointshere
    add sp,-2
    pop hl
    


