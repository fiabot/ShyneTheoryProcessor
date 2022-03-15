# Basic Functions Tests 

# ALU 
ADDI $s0 $0 1   # set $s0 to 1 
ADDI $s1 $0 -1 # set $s1 to -1 
AND $s2 $s0 $s1  # find $s0 AND $s1 
OR $s3 $s0 $s1  # find $s0 OR $s1 

# LW and SW 
Addi $t0 $0 5 # set $1 to 1 
addi $t1 $0 1
SW $t0 0($t1) # store 5 in addr 1 in mem
LW $t2 0($t1) # load addr 1 into $t3