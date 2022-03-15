output_file = "machineCodeOutput.hex"
hex_header = "v2.0 raw"

def get_input():
    imm = input("I? ")
    sw = input("sw? ")
    lw = input("lw? ")
    op = input("op: ")

    par1 = input("par1: ")
    par2 = input("par2: ")
    par3 = input("par3: ")

    return imm + sw + lw + op + par1 + par2 + par3

def main():

    con = input("get machine code? ")

    with open(output_file, "w")  as out:
        out.write(hex_header)
        out.write("\n")
        while con.lower().startswith("y") or con == "1":
            bin = get_input()
            dec = int(bin, 2)
            hexa = hex(dec)
            print(bin, hexa, "\n")

            correct = input("add to hex?")

            if con.lower().startswith("y") or con == "1":
                out.write(hexa[2:])
                out.write("\n")

            con = input("get machine code? ")
    out.close()

main()

