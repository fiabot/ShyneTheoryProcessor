# Insertion Short 
addi $a0 $0 0       # set first address as 0, line 1 
addi $a1 $0 5       # set last address as 6, line 2 
jal recurISort      # run insertion sort, line 3, 4, 5, 6  
j end               # skip to end , line 7 


## insertion sort recursive 
## register use:
##	$a0: parameter: first addr
##	$a1: parameter: last addr 
##  $t0: temp
##	$t1: cur

recurISort:  
    blt $a0 $a1 recur         # recurse is first is less than last, line 8
        jr $ra                  # return, line 9 
	
    recur:addi $sp $sp -3    # make room on stack, line 10  
        sw $ra 0($sp)          # push ra, line 11  
        sw $a0 1($sp)          # push first, line 12  
        sw $a1 2($sp)          # push last, line 13  

        addi $a1 $a1 -1       # last -= 1, line 14  
        jal recurISort          # sort shorter list, line 15, 16, 17, 18  

        lw $a0 1($sp)          # restore first, line 20  
        lw $a1 2($sp)          # retore last, line 21  
        
        lw $t0 0($a1)          # temp = *last, line 23  
        add $t1 $0 $a1           # cur = last, line 24  

        while: bge $a0 $t1 con # if first >= cur exit loop, line 25 
        lw $t2 -1($t1)         # t2 = *(cur - 1), line 26 
        bge $t0 $t2 con       # if temp >= t2 exit, line 27 
            sw $t2 0($t1)      # *cur = *(cur - 1), line 28
            addi $t1 $t1 -1   # cur --, line 29  
            j while             # loop, line 30 
        con: sw $t0 0($t1)     # *cur = temp, line 31  

        lw $ra 0($sp)          # restore ra, line 32
        addi $sp $sp 3       # retore stack, line 33
        jr $ra                  # exit, line 34  

end: # line 35