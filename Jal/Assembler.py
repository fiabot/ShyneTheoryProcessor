# SKELETON ASSEMBLER WRITTEN BY JOHN RIEFFEL
# MODIFY AND ADD YOUR NAME FOR CSC270 FINAL PROJECT

import sys

#from helperfunctions import *
NOOP = "0100000000000000000"
ADDR_SIZE = 4
MAX_IMM = 2 ** ADDR_SIZE
MEM_SIZE = 8
PREAMBLE_LENGTH = 1
REGISTER_DICT = {"0":"0000", "s0":"0001", "s1": "0010", "s2": "0011","s3":"0100", "t0":"0101", "t1":"0110", "t2":"0111",
                 "t3": "1000", "a0":"1001", "a1":"1010", "a2":"1011", "v0":"1100", "v1":"1101", "ra":"1110", "sp":"1111"}

def twosCom(dec, length, add = 0):
    dec = int(dec)
    dec += add
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
    if reg in REGISTER_DICT:
        return REGISTER_DICT[reg]

    reg = int(reg)
    binary = bin(reg).replace("0b", "")

    if len(binary) > length:
        diff = len(binary) - length
        binary = binary[diff:]

    while len(binary) < length:
        binary = "0" + binary
    return binary


def r_inst(operation, operands, opcode_dict, line, labels):
    outstring = ""
    outstring += opcode_dict[operation][1]
    long_str = " ".join(operands)
    if long_str.count("$") != 3:
        print("SYNTAX ERROR AT LINE", line - PREAMBLE_LENGTH)
        return NOOP

    for oprand in operands:
        oprand = oprand.strip()
        if oprand[0] == '$':
            outstring += getBinRegister(oprand[1:], ADDR_SIZE)
    return outstring


def i_inst(operation, operands, opcode_dict, line, labels):
    outstring = ""
    outstring += opcode_dict[operation][1]
    long_str = " ".join(operands)
    if long_str.count("$") != 2:
        print("SYNTAX ERROR AT LINE", line - PREAMBLE_LENGTH)
        return NOOP
    for oprand in operands:
        oprand = oprand.strip()
        if oprand[0] == '$':
            outstring += getBinRegister(oprand[1:], ADDR_SIZE)
        else:
            outstring += twosCom(oprand, ADDR_SIZE)
    return outstring


def dm_inst(operation, operands, opcode_dict, line, labels):
    outstring = ""
    outstring += opcode_dict[operation][1]
    if operands[0][0] == '$':
        outstring += getBinRegister(operands[0][1:], ADDR_SIZE)

    second_operand = operands[1]
    fir_par = second_operand.find("(")
    sec_par = second_operand .find(")")

    if fir_par == -1 or sec_par == -1:
        print("SYNTAX ERROR AT LINE", line - PREAMBLE_LENGTH)
        return NOOP
    else:
        imm = second_operand[:fir_par]
        reg = second_operand[fir_par + 1: sec_par]
        reg = reg.strip()
        outstring += getBinRegister(reg[1:],ADDR_SIZE)
        outstring += twosCom(imm, ADDR_SIZE)
    return outstring


def jump(operation, operands, opcode_dict, line, labels):
    outstring = ""
    outstring += opcode_dict[operation][1]

    # if jumping to label
    dest = operands[0]
    if dest in labels:
        dest = labels[dest]

    outstring += twosCom(dest, MEM_SIZE, add= PREAMBLE_LENGTH)
    outstring += twosCom(0, ADDR_SIZE) # last address not used in jump instructions
    return outstring


def branch(operation, operands, opcode_dict, line, labels):
    outstring = opcode_dict[operation][1]

    long_str = " ".join(operands)
    if long_str.count("$") != 2:
        print("SYNTAX ERROR AT LINE", line - PREAMBLE_LENGTH)
        return NOOP
    # off
    off = operands[2]
    if off in labels: # if branching to label
        off = (labels[off] + PREAMBLE_LENGTH) - line
    outstring += twosCom(off, ADDR_SIZE)

    # ra1
    outstring += getBinRegister(operands[0][1:], ADDR_SIZE)

    # ra2
    outstring += getBinRegister(operands[1][1:], ADDR_SIZE)

    return outstring

def jal(operation, operands, line):
    next_line = line + 3

    lw1 = "addi $ra $0 " + str(line + 2)
    j = "j " + operands[0]

    return [lw, j]

def jr (operation, operands, opcode_dict, line, labels):
    outstring = opcode_dict[operation][1]

    outstring += twosCom(0, ADDR_SIZE) # dest register not used
    outstring += getBinRegister(operands[0][1:], ADDR_SIZE)

    # add offset if given by user
    if len(operands) == 2:
        outstring += twosCom(operands[1], ADDR_SIZE)
    else:
        outstring += twosCom(0, ADDR_SIZE)

    return outstring


def make_label_dict(lines):
    labels = {}
    num = 0
    for i in range(len(lines)):
        line = lines[i]
        line = line.strip()

        label_end = line.find(":")
        if label_end != -1:
            label = line[:label_end]

            labels[label] = num
            line = line[label_end+1:]
            lines[i] = line

        # only increment line if it's not empty space
        if line != "":
            num += 1
    return lines, labels

def de_pseudo(lines, pseudo_dict):
    new_lines = []
    for line in lines:
        outstring = ""
        line = line.strip()
        if line.find('#') != -1:
            line = line[0:line.find('#')]  # get rid of anything after a comment
        if line != '':
            words = line.split()  # assuming syntax words are separated by space, not comma
            operation = words[0]
            operation = operation.lower()
            operands = words[1:]
            if operation in pseudo_dict:
                new_lines += pseudo_dict[operation](operation, operands, len(new_lines) + PREAMBLE_LENGTH)
            else:
                new_lines.append(line)


    return new_lines

def ConvertAssemblyToMachineCode(inline, opcode_dict, line, labels):
    '''given a string corresponding to a line of assembly,
    strip out all the comments, parse it, and convert it into
    a string of binary values'''
    outstring = ""
    inline = inline.strip()
    if inline.find('#') != -1:
        inline = inline[0:inline.find('#')]  # get rid of anything after a comment
    if inline != '':
        words = inline.split()  # assuming syntax words are separated by space, not comma
        operation = words[0]
        operation = operation.lower()
        operands = words[1:]
        outstring = opcode_dict[operation][0](operation, operands, opcode_dict, line, labels)
    return outstring


def preamble(opcode_dict):
    """
    return the list of instructions that are run every program
    :param opcode_dict: dictionary of opcodes and coresponding instructions
    :return: a list of machine code to run each program
    """
    codes = []
    stack = "addi $sp $0 -1" # set sp to last mem address
    codes.append(binToHex(ConvertAssemblyToMachineCode(stack, opcode_dict, 0, {})))
    return codes


def binToHex(bin):
    dec = int(bin, 2)
    hexa = hex(dec)
    hexa = hexa.replace("0x", "")
    return hexa


def opcodes():
    opcode_dict = {'add': (r_inst, '0000000'), "sub": (r_inst, "0000011"), "or": (r_inst, "0000010"),
                   "and": (r_inst, "0000001")}
    immediates = {'addi': (i_inst, '0100000'), 'subi': (i_inst, '0100011'), 'ori': (i_inst, '0100010'),
                  'andi': (i_inst, '010001')}
    dm = {"lw": (dm_inst, "0101000"), "sw": (dm_inst, "0110000")}
    branches = {"j" : (jump, "1000000"), "beq" : (branch, "1000100"), "bne" : (branch, "1000101"), "blt" : (branch, "1000110"), "bge" : (branch, "1000111"), "jr": (jr, "1100000")}
    pseudo = {"jal": jal}
    opcode_dict.update(immediates)
    opcode_dict.update(dm)
    opcode_dict.update(branches)
    return opcode_dict, pseudo


def AssemblyToHex(infilename, outfilename):
    '''given an ascii assembly file , read it in line by line and convert each line of assembly to machine code
    then save that machinecode to an outputfile'''

    opcode_dict, pseudo = opcodes()
    outlines = preamble(opcode_dict)
    line = len(outlines)
    header = "v2.0 raw\n"
    with open(infilename) as f:
        lines = [line.rstrip() for line in f.readlines()]  # get rid of \n whitespace at end of line
        lines = de_pseudo(lines, pseudo)
        lines, labels = make_label_dict(lines)
        print(lines, labels)
        for curline in lines:
            outstring = ConvertAssemblyToMachineCode(curline, opcode_dict, line, labels)
            if isinstance(outstring, list):
                for inst in outstring:
                    outlines.append(binToHex(inst))
                    line += 1
            elif outstring != '':
                outlines.append(binToHex(outstring))
                line += 1
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
        outstring = ConvertAssemblyToMachineCode(line, opcode_dict, 0)
        hexa = ""
        if outstring != '':
            dec = int(outstring, 2)
            hexa = hex(dec)
            hexa = hexa.replace("0x", "")

        print(outstring, hexa)

        con = input("continue? ")


if __name__ == "__main__":
    main()