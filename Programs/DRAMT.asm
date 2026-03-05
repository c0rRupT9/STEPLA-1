; Register Jugglers
.define base 5
.define exp 3

init:
    MOVI RA, base
    MOVI RB, exp
    MOVI RC, base    ; Start with 5
    
    ; If exponent is 1, we are done
    MOVI RD, 1
    SUB  RB, RD
    JZ   display

outer_loop:
    ; 1. Save current Total (RC) as the value we will add in this round
    STIM RC, 250     
    
    ; 2. We need to add RC to itself (Base - 1) times.
    ; We need a counter. Let's use RD.
    MOV  RD, RA      ; RD = 5
    MOVI RC, 1       ; Use RC temporarily to hold '1'
    SUB  RD, RC      ; RD = 4 (Inner Counter)
    
    ; 3. Restore RC from memory to start adding
    LDIM RC, 250

inner_multiply:
    ; We need to add the saved value to RC. 
    ; But we need a register to hold the saved value!
    ; We will use RA (since base is constant, we can reload it later)
    LDIM RA, 250     ; RA now holds the 'Addend'
    ADD  RC, RA      ; RC = RC + Addend
    MOVI RA, base    ; Restore RA for the next round
    
    ; 4. Decrement Inner Counter (RD)
    ; We need a '1'. Let's borrow RA's value or MOVI.
    MOVI RA, 1       ; Temporary 1
    SUB  RD, RA
    MOVI RA, base    ; Restore Base
    
    JZ   check_exponent
    JMP  inner_multiply

check_exponent:
    MOVI RD, 1       ; Temporary 1
    SUB  RB, RD      ; Decrement Outer Counter
    JZ   display
    JMP  outer_loop

display:
    OUT  RC          ; Should show 7D (125)
    HLT