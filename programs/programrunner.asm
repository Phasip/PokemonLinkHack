INCLUDE "red/main.asm"
SECTION "Nobank",ROMX,BANK[$ff]
Func_216be EQU $56be ;Not global, and declared from audio.asm...
Func_216be_Bank EQU $8 ;Not global, and declared from audio.asm...
;Serial_Exchange_Bytes EQU $216f
STARTLABL::
    db $53
    db $54
    db $41
    db $52
    db $54
SomeLabel::
    ld a,Func_216be_Bank
    call BankswitchHome
    ld hl,W_NUMINBOX
    call Func_216be ; listpokemon
    call BankswitchBack
    jr nc,.runcode ; Flags should be non-modified in Bankswitchback
    ret
.runcode
    ld hl,wBoxMon1+1 ;One byte into pokemon. avoid pokemon id
    ld a,[wWhichPokemon]
    ld bc,wBoxMon2-wBoxMon1
    call AddNTimes
    jp [hl]
ENDLABL::
    db $45
    db $4e
    db $44

