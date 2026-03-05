; Calculate Fib values
; DRAM -> store
; access it -> display


start:
MOVI RA, 1    ; Current number
MOVI RB, 1    ; Next number
MOVI RD, 254 ; Adress Pointer

fib_loop:
    OUT RA    ; Display current
    STRD [RD], RA ; Store Contents of RA at DRAM[RD]
    STIM RC, [10] ; Store RC temporarily
    MOVI RC, 2 ; Pointer decrement constant
    SUB RD, RC 
    LDIM RC, [10] ; Return RC to its original state
    MOV RC, RA ; Save Current to Temp
    ADD RA, RB ; Current = Current + Next   
    MOV RB, RC ; Next = Old Current 
    JC RDinit   ; If we exceed 255 (Carry set)
    JMP fib_loop

RDinit: ; initialize for Looping, Move Increment Constant to RC
    STIM RD, [1]
    MOVI RC, 2
    JMP DisplayFromRAM

LoadRD: 
    LDIM RD, [1]

DisplayFromRAM:
    LDD [RD], RA
    OUT RA
    ADD RD, RC
    JC LoadRD
    JMP DisplayFromRAM
