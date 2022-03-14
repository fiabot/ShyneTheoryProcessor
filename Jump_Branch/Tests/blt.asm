blt $2 $3 3          # line 6 
    # if $2 >= 3 
    sw $3 0($0)     # line 7
    j 10             # line 8
# else ($2 < $3)
lw $2 0($0)         # line 9 