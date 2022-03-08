# add first four values in memory
# $1: length, $2: i, $3 sum, $4 temp 
addi $1 $0 4 
addi $2 $0 0
addi $3 $0 0 

beq $1 $2 5  
lw $4 0($2)
add $3 $3 $4 
addi $2 $2 1 
j 3 
