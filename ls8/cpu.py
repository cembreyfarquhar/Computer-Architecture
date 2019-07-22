"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 0xff
        self.reg = [0] * 0x08
        self.pc = 0x00
        self.MAR = 0  # Memory addrress for reading or writing to
        self.MDR = 0  # value to write or that was just read
        self.fl = 0


    def ram_read(self, MAR):
        # print(f'READ ADDRESS: {read_address}')
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # open file 
        with open(sys.argv[1]) as file:
            for line in file:
                if line[0] != '#' and line != '\n':
                    # if line is not comment or new line, print binary of line to ram
                    self.ram[address] = int(line[0:8], 2)
                    address += 1
            file.close
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.IR = self.pc
        self.trace()

        # opcodes
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111

        running = True

        while running:
            self.IR = self.pc
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # exit condition
            if self.ram[self.IR] == HLT:
                running = False
            elif self.ram[self.IR] == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif self.ram[self.IR] == PRN:
                print(self.reg[operand_a])
                self.pc += 2

