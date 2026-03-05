; --- CONSTANTS ---
.define START_VAL 1
.define MAX_COUNT 5

; --- INITIALIZATION ---
MOVI RA, 0           ; RA = Accumulator (Current Sum)
MOVI RB, START_VAL   ; RB = Counter (1, 2, 3...)
MOVI RC, 1           ; RC = Incrementer (Always 1)

main_loop:
    OUT RA           ; Output the current sum
    ADD RA, RB       ; RA = RA + RB
    
    ; Logic to check if we are done
    ; We subtract 1 from a temp RD to see if RB has reached MAX_COUNT
    MOVI RD, MAX_COUNT
    SUB RD, RB       ; If RD == RB, then RD becomes 0
    JZ end_program   ; If Zero flag is set, we are finished
    
    ADD RB, RC       ; Increment our counter (RB++)
    JMP main_loop    ; Repeat

end_program:
    OUT RA           ; Output final result (Should be 0x0F / 15)
    HLT              ; Stop the CPU