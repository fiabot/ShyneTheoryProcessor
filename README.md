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
Anything following the hashtag (#) symbol is ignored by the assembler.
R instructions
R instructions are written in the following format:
````
add $dest $ra1 $ra2
```` 
 
where the computation done on $ra1 and $ra2 will be placed in $dest. The following r instructions are available.
add: add the contents of $ra1 and $ra2
sub: subtract the contents of $ra2 from $ra1
or: compute logical or on $ra1 and $ra2
and: compute logical and on $ra1 and $ra2
 
Example:
````
add $1 $1 $2 # set $1 to $1 + $2 
````
 
I instructions
I instructions are written in the following format:
addi $dest $ra1 imm
 
where the computation done on $ra1 and the value imm will be placed in $dest. The following i instructions are available. The value imm can only be an integer from -8 to 7. 

addi: add the contents of $ra1 and the value imm
subi: subtract imm from $ra1
ori: compute logical or on $ra1 and the value imm
andi: compute logican and on $ra1 and the value imm
Sll: shift the value of $ra1 to the left by imm bits
Slr: shift the value of $ra2 to the right by imm bits  
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
j n # jump to the (n + 1)th instruction  
 
Instructions start at 0, and comments and empty spaces are not counted. Any instructions added in the assembler are adjusted for, meaning j 0 will go to the first instruction in the .asm file, not the first instruction the processor runs. 

## Branch Instructions
Branch instructions take the following format:
````
beq $ra1 $ra2 OFF # skip to current instruction + OFF if $ra1 == $ra2 
````
 
Branch instructions move the program counter by the amount specified by OFF, meaning that a branch with offset 1 will move the program forward the same as what would occur had a branch not taken place. The following branch instructions are available:
beq: branch if the two registers are equal
bne: branch if the two registers are not equal
blt: branch if the first register is less than the second
bge: branch if the first register is greater than or equal to the second
 
### The Stack 
Assembler.py will set the initial value of $sp to the last value of data memory (jump instructions are adjusted to account for this initial instruction, so you can write j instructions as if the first line in the assembly file is instruction 0). 

You can push values on to the stack with the following format: 
````
	Addi $sp $sp -1 
	sW $reg 0($sp) 
 ````

You can pop values from the stack with the following format: 
````
LW $dest 0($sp) 
Addi $sp $sp 1
````

### Jal Instructions 
The jal instruction is not a direct machine code instruction, but instead a pseudo instruction produces 4 machine instruction when assembled. The first 3 of these are used to store the next instruction address after the jal instruction into the register $ra. Since immediate instructions can only handle up to the number 7, this is done by first loading the first 4 bits into $ra, then right shifting it by 4, before adding the least significant bits. The last instruction jumps the program counter to the instruction specified.  

````
Jal 6 # store next line and jump to line 6  
```` 

### Jr Instructions 
Jr instructions take the following formats: 
````
Jr $reg # jump to instruction at line $reg 
Jr $reg 1 # jump to instruction at line $reg + 1 
````

This is most useful for returning to the instruction stored in $ra after a Jal instruction is called. 

````
Jr $ra  
```` 

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

### Insertion Sort 
This shows how you can implement recursive insertion sort 
````  
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
````  




