; --- UNIVERSAL POWER (4 REGS) ---
MOVI RA, 5      ; Base (X)
MOVI RB, 2      ; Exponent (Y)
MOVI RC, 1      ; Result Accumulator (Start at 1)

outer_loop:
    ; Check if Exponent is done
    MOVI RD, 1
    SUB  RB, RD     ; RB = RB - 1
    JC   finish     ; If Carry/Borrow happens, we are done
    JZ   finish     ; If 0, we are done

    ; Multiplication: New_RC = Old_RC * Base(RA)
    MOV  RD, RC     ; RD = The value to be added (the "running total")
    MOV  rs, RA     ; We need an inner counter set to 'Base'
    ; Since we only have 4 regs, we'll use 'RB' as the inner counter
    ; BUT we must save the 'Outer RB' to DRAM first!