# Label Test 
# every instruction adding to s0 should be skipped 
# every instruction adding to s1 should be ran 
addi $s0 $0 0               # line 1 
addi $s1 $0 1               # line 2 

# j instruction 
j branch                    # line 3 
addi $s0 $s0 1              # line 4 

# branch instruction 
branch: addi $s1 $s1 1     # line 5 
bne $s0 $s1 neq            # line 6 
addi $s0 $s0 1             # line 7 
addi $s0 $s0 1             # line 8
neq: addi $s1 $s1 1        # line 9 

# jal 
jal last                   # line a 
add $s2 $s1 $s1            # line c
j end                      # line d 

last: addi $s1 $s1 1       # line e 
jr $ra                     # line f

end: add $0 $0 $0          # line 10 
