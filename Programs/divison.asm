.define dividend 48
.define divisor 2

start:
MOVI RA, dividend
out RA
MOVI RB, divisor
out RB
MOVI RC, 1
MOVI RD, 0

init:
add RD, RC
sub RA, RB
jz end
jmp init

end:
out RD 
hlt