movi ra, 2 ; Multiplicand
movi rb, 100 ; Multiplicator
movi rc, 1 ; decrement constant
movi rd, 0 ; INITIALIZATION

main_loop: 
add rd, ra 
sub rb, rc
jz exit ; exit only if last operation had a result of zero
jmp main_loop ; if not jumped yet jump back to main_loop


exit:
out rd
hlt
