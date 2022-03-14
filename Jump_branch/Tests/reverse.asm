Addi $t0 $0 5 # $t0 contains the last element  
Lw $t1 0($0)  
LW $t2 0($t0) # load the first and last elements into $t1 and $t2 
Sw $t1 0($t0) 
SW $t2 0($0) # swap first and last 

Lw $t1 1($0)  
LW $t2 -1($t0) 
Sw $t1 -1($t0) 
SW $t2 1($0)  

Lw $t1 2($0) # repeat with second first/last 
LW $t2 -2($t0) 
Sw $t1 -2($t0)  
SW $t2 2($0) # swap 3rd and 4th  
