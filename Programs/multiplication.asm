; Multiply RA (multiplicand) × RB (multiplier) → result in RC
movi rc, 0          ; product = 0
movi rd, 8          ; bit counter
shift_add_loop:
    jc add_bit      ; if LSB of RB is 1 (carry from previous test)
    jmp skip_add
add_bit:
    add rc, ra      ; product += multiplicand
skip_add:
    add ra, ra      ; multiplicand <<= 1 (×2)
    add rb, rb      ; multiplier <<= 1 (or use SUB + JC to test LSB)
    sub rd, 1
    jnz shift_add_loop