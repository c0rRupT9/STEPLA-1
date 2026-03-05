; Count till overflow and then count back down till zero
; defining variables
.define init 0
.define valinc 2



initialize: ; 0
movi RA, init ; initialize the values by moving them immideately
movi RB, valinc

add_loop:
out RA
add RA, RB
jc sub_loop
jmp add_loop

sub_loop:
out RA
sub RA, RB
jz initialize
jmp sub_loop