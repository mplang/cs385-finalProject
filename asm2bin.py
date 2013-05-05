"""
asm2bin.py

Author: Michael P. Lang
Date:   4 May 2013

Converts 16-bit mini pipelined MIPS assembly code to hex code for use as
instruction input to the CPU. Binary representation of the hexadecimal values
are supplied as comments in the output file.
"""


import sys
from bitstring import BitArray

opcodes = {"add": {"op": "0000", "type": "r"},
           "sub": {"op": "0001", "type": "r"},
           "and": {"op": "0010", "type": "r"},
           "or": {"op": "0011", "type": "r"},
           "addi": {"op": "0100", "type": "i"},
           "lw": {"op": "0101", "type": "m"},
           "sw": {"op": "0110", "type": "m"},
           "slt": {"op": "0111", "type": "r"},
           "beq": {"op": "1000", "type": "i"},
           "bne": {"op": "1001", "type": "i"},
           "sll": {"op": "1010", "type": "s"},
           "srl": {"op": "1011", "type": "s"},
           "j": {"op": "1100", "type": "j"},
           "nop": {"op": "0000", "type": "n"}}

registers = {"$0": "00", "$1": "01", "$2": "10", "$3": "11"}

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as in_file:
        with open(sys.argv[2], 'w') as out_file:
            for line in in_file:
                line = line[:line.find('#')].strip()
                if not line or line.find(':') != -1 or line[0] == '.':
                    continue
                opcode = ''
                rs = ''
                rt = ''
                rd = ''
                value = ''
                shamt = ''
                bin_line = ''
                tokens = line.lower().split(' ')
                tokens = tokens[:1] + ''.join(tokens[1:]).split(',')
                opcode = opcodes[tokens[0]]["op"]
                optype = opcodes[tokens[0]]["type"]
                print(tokens)
                if optype == 'r':
                    rd = registers[tokens[1]]
                    rs = registers[tokens[2]]
                    rt = registers[tokens[3]]
                    value = "000000"
                elif optype == 'i':
                    rt = registers[tokens[1]]
                    rs = registers[tokens[2]]
                    value = BitArray(int=int(tokens[3]), length=8).bin
                elif optype == 'm':
                    rt = registers[tokens[1]]
                    rs_begin = tokens[2].find('(')
                    rs_end = tokens[2].find(')')
                    value = BitArray(int=int(tokens[2][:rs_begin]),
                                     length=8).bin
                    rs = registers[tokens[2][rs_begin+1:rs_end]]
                elif optype == 's':
                    rs = "00"
                    rd = registers[tokens[1]]
                    rt = registers[tokens[2]]
                    shamt = BitArray(int=int(tokens[3]), length=4).bin
                    value = "00"
                elif optype == 'j':
                    rs = "00"
                    rt = "00"
                    value = BitArray(int=int(tokens[1]), length=8).bin
                else:
                    # nop
                    rs = "00"
                    rt = "00"
                    rd = "00"
                    value = "000000"

                bin_line = ''.join((opcode, rs, rt, rd, shamt, value))
                hex_line = BitArray("0b" + bin_line).hex
                if optype == 'n' or optype == 'j':
                    out_file.write("{}\t// {}\t\t\t==> {}\n".
                                   format(hex_line,
                                   line.lower(),
                                   bin_line))
                elif optype == 'm':
                    out_file.write("{}\t// {}\t\t==> {}\n".
                                   format(hex_line,
                                   line.lower(),
                                   bin_line))
                else:
                    out_file.write("{}\t// {}\t==> {}\n".
                                   format(hex_line,
                                   line.lower(),
                                   bin_line))
