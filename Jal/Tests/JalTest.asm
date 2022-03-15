# Test JAL and JR 

addi $s0 $0 1           # set s0 to 1, line 0  
jal 5                   # jal line 5, line 1
                        # invisble line for jal, line 2               
add $s2 $s0 $s1         # add s0 and s3, line 3 
j 7                     # skip to end, line 4 

# destination of line 1
addi $s1 $0 4          # set s1 to 4, line 5 
jr $ra                 # return to orginal, line 6   

