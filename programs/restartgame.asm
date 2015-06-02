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
MyCode:: ;First we copy the data we have to a place that won't be reset
    call HandlePartyMenuInput-1
.hladdr   ; Hl points here now
    dec sp ;Avoid FE in add sp,-2
    dec sp
    pop hl
    ld b,0
    ld c,.restcode-.hladdr
    add hl,bc
    ld bc,.bagend-.restcode
    
    ld de,PLACECODE
    call CopyData
    jp PLACECODE
.restcode
    xor a ;Then we run the initialization with oaks speech
    ld b,a
    inc a
    ld [wcc47],a ; Do not jump into world instantly
    ld b, BANK(Func_5d52)
	ld hl, Func_5d52 ; New game button press
	call Bankswitch
    
    ld hl,PLACECODE+(.bagdata-.restcode) ;When the speech is finished we give some items
    ld de,wNumBagItems
    ld bc,.bagend-.bagdata
    call CopyData
    jp EnterMap ; Finally start the game
.bagdata
    db $03
    db $01
    db $06
    db $5D
    db $01
    db $7A
    db $63
    db $FF
.bagend
    
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
    


