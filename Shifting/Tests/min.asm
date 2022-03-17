# put the smallest number of $1, $2, $3 in first memory address

bge $1 $2 6        # line 0
    # if $1 < $2 
    bge $1 $3 3     # line 1
        # if $1 < $3 
        sw $1 0($0) # line 2 
        j 10         # line 3 
    # else ($1 >= 3)
    sw $3 0($0)     # line 4 
    j 10              # line 5
# else ($1 >= $2)
blt $2 $3 3          # line 6 
    # if $2 >= 3 
    sw $3 0($0)     # line 7
    j 10             # line 8
# else ($2 < $3)
sw $2 0($0)         # line 9 
