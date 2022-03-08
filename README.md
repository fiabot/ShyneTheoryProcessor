# ShyneTheoryProcessor
8-bit processor 

A bit bit processor cabable of addition, subtraction, and logic commands. 16 registers can be accessed with $0 - $15. There is capacity for 256 bytes in data memory and programs with up to 256 instructions. 

## Assembly Language 
Assembly code can be assembled to hex values that can be feed into the processor by running Assembler.py in the command line and passing in an .asm and .hex file. The program in the .asm will be tranlated to machine code and placed in the .hex file to be read by the processor. 

###  R instructions 
R instructions are written in the following format: 

````
add $dest $ra1 $ra2
```` 

where the computation done on $ra1 and $ra2 will be placed in $dest. The following r instructions are available. 


add: add the contents of $ra1 and $ra2

sub: subtract the contents of $ra2 from $ra1 

or: compute logical or on $ra1 and $ra2 

and: compute logican and on $ra1 and $ra2 

Example: 
````
add $1 $1 $2 # set $1 to $1 + $2 
```` 

###  I instructions 
I instructions are written in the following format: 

````
addi $dest $ra1 imm
```` 

where the computation done on $ra1 and the value imm will be placed in $dest. The following i instructions are available. 


addi: add the contents of $ra1 and the value imm

subi: subtract imm from $ra1

ori: compute logical or on $ra1 and the value imm 

andi: compute logican and on $ra1 and the value imm

Example: 
````
addi $1 $0 1 # set 1 to $0 + 1 
```` 

### Data Memory 
Values can be loaded and stored into memory with the lw and sw commands. 

Load word (lw) takes loads a word (8 bits) into the destination register, by adding the value within a base register to an offset value. Load words take the following format. 
````
lw $dest offset($ba)
```` 

Similarly, store word (sw) takea a word from a source register and stores into data memory at the address speficied by a base register and an offset value. Storw words take the following format. 

Example: 
````
SW $1 1($0) # store the value at $1 into data memory at $0 + 1 
LW $3 1($0) # load the value at data memory $0 + 1 into $1 
````

### Reverse Example 
The following code reverses a 6 element array that stores it's first element at the address in $0. 

````
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
````




