# SKELETON ASSEMBLER WRITTEN BY JOHN RIEFFEL
# MODIFY AND ADD YOUR NAME FOR CSC270 FINAL PROJECT

import sys

#from helperfunctions import *
NOOP = "10000000000000000"
ADDR_SIZE = 4
MEM_SIZE = 8

def twosCom(dec, length):
    dec = int(dec)
    if dec < 0:
        max_num = 2 ** length - 1
        dec = max_num - (-dec - 1)
    binary = bin(dec).replace("0b", "")

    if len(binary) > length:
        diff = len(binary) - length
        binary = binary[diff:]

    while len(binary) < length:
        binary = "0" + binary
    return binary

def getBinRegister(reg, length):
    # converting decimal to binary
    # and removing the prefix(0b)
    reg = int(reg)
    binary = bin(reg).replace("0b", "")

    if len(binary) > length:
        diff = len(binary) - length
        binary = binary[diff:]

    while len(binary) < length:
        binary = "0" + binary
    return binary


def r_inst(operation, operands, opcode_dict):
    outstring = ""
    outstring += opcode_dict[operation][1]
    long_str = " ".join(operands)
    if long_str.count("$") != 3:
        print("SYNTAX ERROR")
        return NOOP

    for oprand in operands:
        oprand = oprand.strip()
        if oprand[0] == '$':
            outstring += getBinRegister(oprand[1:], ADDR_SIZE)
    return outstring


def i_inst(operation, operands, opcode_dict):
    outstring = ""
    outstring += opcode_dict[operation][1]
    long_str = " ".join(operands)
    if long_str.count("$") != 2:
        print("SYNTAX ERROR")
        return NOOP
    for oprand in operands:
        oprand = oprand.strip()
        if oprand[0] == '$':
            outstring += getBinRegister(oprand[1:], ADDR_SIZE)
        else:
            outstring += twosCom(oprand, ADDR_SIZE)
    return outstring

def dm_inst(operation, operands, opcode_dict):
    outstring = ""
    outstring += opcode_dict[operation][1]
    if operands[0][0] == '$':
        outstring += getBinRegister(operands[0][1:], ADDR_SIZE)

    second_operand = operands[1]
    fir_par = second_operand.find("(")
    sec_par = second_operand .find(")")

    if fir_par == -1 or sec_par == -1:
        print("SYNTAC ERROR")
        return NOOP
    else:
        imm = second_operand[:fir_par]
        reg = second_operand[fir_par + 1: sec_par]
        reg = reg.strip()
        outstring += getBinRegister(reg[1:],ADDR_SIZE)
        outstring += twosCom(imm, ADDR_SIZE)
    return outstring


def jump(operation, operands, opcode_dict):
    outstring = ""
    outstring += opcode_dict[operation][1]

    outstring += twosCom(operands[0], MEM_SIZE)
    outstring += twosCom(0, ADDR_SIZE)
    return outstring

def branch(operation, operands, opcode_dict):
    outstring = opcode_dict[operation][1]

    long_str = " ".join(operands)
    if long_str.count("$") != 2:
        print("SYNTAX ERROR")
        return NOOP
    # off
    outstring += twosCom(operands[2], ADDR_SIZE)

    # ra1
    outstring += getBinRegister(operands[0][1:], ADDR_SIZE)

    # ra2
    outstring += getBinRegister(operands[1][1:], ADDR_SIZE)

    return outstring

def ConvertAssemblyToMachineCode(inline, opcode_dict):
    '''given a string corresponding to a line of assembly,
    strip out all the comments, parse it, and convert it into
    a string of binary values'''
    outstring = ""
    if inline.find('#') != -1:
        inline = inline[0:inline.find('#')]  # get rid of anything after a comment
    if inline != '':
        words = inline.split()  # assuming syntax words are separated by space, not comma
        operation = words[0]
        operation = operation.lower()
        operands = words[1:]
        outstring = opcode_dict[operation][0](operation, operands, opcode_dict)
    return outstring

def opcodes():
    opcode_dict = {'add': (r_inst, '0000000'), "sub": (r_inst, "0000011"), "or": (r_inst, "0000010"),
                   "and": (r_inst, "0000001")}
    immediates = {'addi': (i_inst, '0100000'), 'subi': (i_inst, '0100011'), 'ori': (i_inst, '0100010'),
                  'andi': (i_inst, '010001')}
    dm = {"lw": (dm_inst, "0101000"), "sw": (dm_inst, "0110000")}
    branches = {"j" : (jump, "1000000"), "beq" : (branch, "1000100"), "bne" : (branch, "1000101")}
    opcode_dict.update(immediates)
    opcode_dict.update(dm)
    opcode_dict.update(branches)
    return opcode_dict

def AssemblyToHex(infilename, outfilename):
    '''given an ascii assembly file , read it in line by line and convert each line of assembly to machine code
    then save that machinecode to an outputfile'''

    opcode_dict = opcodes()
    outlines = []
    header = "v2.0 raw\n"
    with open(infilename) as f:
        lines = [line.rstrip() for line in f.readlines()]  # get rid of \n whitespace at end of line
        # if you are a python ninja, use list comprehension. and replace the for loop below
        # with this expression
        # outlines = [ConvertAssemblyToMachineCode(curline) for curline in lines]
        # but, no judgement if you prefer explicit for loops
        for curline in lines:
            outstring = ConvertAssemblyToMachineCode(curline, opcode_dict)
            if outstring != '':
                dec = int(outstring, 2)
                hexa = hex(dec)
                hexa = hexa.replace("0x", "")
                outlines.append(hexa)

    f.close()

    with open(outfilename, 'w') as of:
        of.write(header)
        for outline in outlines:
            of.write(outline)
            of.write("\n")
    of.close()

def main():
    # in order to run this with command-line arguments
    # we need this if __name__ clause
    # and then we need to read in the subsequent arguments in a list.

    #### These two lines show you how to iterate through arguments ###
    #### You can remove them when writing your own assembler
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))

    ## This is error checking to make sure the correct number of arguments were used
    ## you'll have to change this if your assembler takes more or fewer args
    if (len(sys.argv) != 3):
        print('usage: python skeleton-assembler.py inputfile.asm outputfile.hex')
        exit(0)
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    AssemblyToHex(inputfile, outputfile)

def line_test():
    opcode_dict = opcodes()

    con = input("convert assembly? ")

    while con.lower().startswith("y") or con == "1":
        line = input("Assemby: ")
        outstring = ConvertAssemblyToMachineCode(line, opcode_dict)
        hexa = ""
        if outstring != '':
            dec = int(outstring, 2)
            hexa = hex(dec)
            hexa = hexa.replace("0x", "")

        print(outstring, hexa)

        con = input("continue? ")


if __name__ == "__main__":
    main()