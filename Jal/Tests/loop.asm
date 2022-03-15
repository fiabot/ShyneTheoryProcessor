# add first four values in memory
# $s0: length, $s1: i, $s2 sum, $s3 temp 
addi $s0 $0 4 
addi $s1 $0 0
addi $s2 $0 0 

beq $s0 $s1 5  
lw $s3 0($s1)
add $s2 $s2 $s3 
addi $s1 $s1 1 
j 3 
