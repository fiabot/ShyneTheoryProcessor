# ShyneTheoryProcessor
8-bit processor 

A bit bit processor cabable of addition, subtraction, and logic commands. 16 registers can be accessed with $0 - $15. There is capacity for 256 bytes in data memory and programs with up to 256 instructions. 

## How To Use 
The full processor is located in the jump_branch folder. The processor itself is the jump_branch.circ file which can be loaded into logisim. Programs can be loaded as hex files into the instruction memory circuit. Once loaded, the program can be steped through by enabling instruction memory and giving the clock a rising clock edge. Assembly code can be translated to hex files by running Assembler.py in the command line with the following command. 

````
python Assembler.py "ASSEMBLY_FILE" "HEX_FILE"
```` 

## Assembly Language 
Assembly code can be assembled to hex values that can be feed into the processor by running Assembler.py in the command line and passing in an .asm and .hex file. The program in the .asm will be tranlated to machine code and placed in the .hex file to be read by the processor. 

### Registers 
Registers can be accessed either through the number or by label. 

| Register | Label | Use |
| ------------- | ------------- | ------------- |
$0 | $0 | Should contain the value 0 
$1  |$s0 | Protected variable
$2 |$s1 | Protected variable
$3 |$s2 | Protected variable
$4 |$s3 | Protected variable
$5 |$t0 | Unprotected variable
$6 |$t1 | Unprotected variable
$7 |$t2 | Unprotected variable
$8  |$t3 | Unprotected variable
$9 |$a0 | Argument 
$10 |$a1 | Argument
$11 |$a2 | Argument
$12 |$v1 | Return value 
$13 |$v2 | Return value 
$14 |$ra | Return address
$15 |$sp | stack pointer

### Comments 
Anything following the hashtag symbol is ignored by the assembler. 

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

Similarly, store word (sw) takes a word from a source register and stores it into data memory at the address specified by a base register and an offset value. Store words take the following format.

Example: 
````
SW $1 1($0) # store the value at $1 into data memory at $0 + 1 
LW $3 1($0) # load the value at data memory $0 + 1 into $1 
````

### Jump Instructions 
You can jump to any line of instruction memory with the instruction:  
````
j n # jump to the (n + 1)th instruction  
````

Instructions start at 0, and comments and empty spaces are not counted. 

### Branch Instructions 
Branch instructions take the following format: 
````
beq $ra1 $ra2 OFF # skip to instruction + OFF if $ra1 == $ra2 
````

Branch instructions move the program counter by the amount specified by OFF, meaning that a branch with offset 1 will move the program forward the same as what would occur had a branch not taken place. The following branch instructions are available:

beq: branch if the two registers are equal 

bne: branch if the two registers are not equal 

blt: branch if the first register is less than the second 

bge: branch if the first register is greater than or equal to the second 


## Examples 
Example assembly code and correspodning hex files can be found in the Tests folder. 

### Reverse 
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

### Loop
The following code adds the first four values in memory in a loop 

```` 
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
````

### Stack 
The following codes shows how to push and pop from the stack 

````
# set up initial variables 
addi $s0 $0 1 
addi $s1 $0 5 

# push on to stack 
addi $sp $sp -2 
sw $s0 0($sp)
sw $s1 1($sp)

# pop from stack 
lw $t0 0($sp)
lw $t1 1($sp)
addi $sp $sp 2 
```` 





