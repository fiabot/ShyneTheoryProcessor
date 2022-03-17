# stack test 

# set up initial variables 
addi $s0 $0 1 
addi $s1 $0 5 

# push on to stack 
addi $sp $sp -2 
sw $s0 0($sp)
sw $s1 1($sp)

# pop from stack 
lw $t0 0($sp)
lw $t1 1($sp)
addi $sp $sp 2 


