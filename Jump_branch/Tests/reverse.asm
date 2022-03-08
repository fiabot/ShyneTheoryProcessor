Addi $1 $0 5 # $1 contains the last element  
Lw $2 0($0)  
LW $3 0($1) # load the first and last elements into $2 and $3 
Sw $2 0($1) 
SW $3 0($0) # swap first and last 

Lw $2 1($0)  
LW $3 -1($1) 
Sw $2 -1($1) 
SW $3 1($0)  

Lw $2 2($0) # repeat with second first/last 
LW $3 -2($1) 
Sw $2 -2($1)  
SW $3 2($0) # swap 3rd and 4th  
