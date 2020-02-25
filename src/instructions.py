from enum import Enum
from .cpu_types import *

class Addressing(Enum):
    """Enum for establishing the instruction operand Addressing mode"""
    # Operand is a constant value (which is *not* immediate)
    Constant = 'c'

    # Operand is CPU bit value
    Bit = 'b'

    # Operand value is in the instruction
    Immediate = 'I'

    # Uses a CPU register as value
    Register = 'R'

    # Uses value and does R+1
    RegisterIncrement = 'R+'
    # Uses value and does R-1
    RegisterDecrement = 'R-'

    # Uses the Register + what is given by the operand
    RegisterPlusImmediate = 'RI'

    # Uses the register as an indirection for the value
    RegisterIndirect = 'Ri'

    # Operand location is in the instruction
    # Value is obtained by dereferencing
    Direct = 'D'

    # Operand pointer is at location
    Indirect = 'i'
#end bits

class Operand:
    """
    Internal representation of an instruction operand
    This is used both for binding (get/set) and debugging purposes
    """

    def __init__(self, reg, width, addressing_mode):
        self.width = width
        self._mode = addressing_mode
        self._register = reg

    @staticmethod
    def reg(reg, width=1):
        return Operand(reg, width, Addressing.Register)

    @staticmethod
    def regi(reg, width=1):
        return Operand(reg, width, Addressing.RegisterIndirect)

    @staticmethod
    def regI(reg):
        return Operand(reg, 1, Addressing.RegisterPlusImmediate)

    @staticmethod
    def imm(width):
        return Operand(None, width, Addressing.Immediate)

    @staticmethod
    def mem(width):
        return Operand(reg, width, Addressing.Direct)

    def can_set_value(self):
        """Checks if this operand can be used to set value"""
        return self._mode != Addressing.Immediate and self._mode != Addressing.RegisterPlusImmediate

    def get_value(self, cpu, mem_bus, location):
        "Gets the value of the operand"

        # Methods that will get the value
        def immediate():
            return mem_bus.ReadWorkRAM(location, self.width)
        def register():
            if self._register < 0:
                return cpu.SP if self._register == Registers.SP else cpu.PC
            return cpu.get_register(self._register, self.width)
        def register_post():
            value = register()
            # the set will increment/decrement as needed
            self.set_value(cpu, mem_bus, location, value)
            return value
        def register_w_immediate():
            return register() + immediate()
        def reg_indirect():
            return mem_bus.ReadWorkRAM(register(), self.width)
        def direct():
            return mem_bus.ReadWorkRAM(immediate(), self.width)
        def indirect():
            return mem_bus.ReadWorkRAM(direct(), self.width)

        value_map = {
            Addressing.Immediate: immediate,
            Addressing.Register: register,
            Addressing.RegisterIncrement: register_post,
            Addressing.RegisterDecrement: register_post,
            Addressing.RegisterPlusImmediate: register_w_immediate,
            Addressing.RegisterIndirect: reg_indirect,
            Addressing.Direct: direct,
            Addressing.Indirect: indirect}

        retVal = value_map[self._mode]()
        if type(retVal) is bytearray:
            retVal = int.from_bytes(retVal, 'big')
        return retVal
    #end get_value

    def set_value(self, cpu, mem_bus, location, value):
        "Sets the value of the operand. Use for writeback step"
        # Methods that will get the value
        def immediate():
            raise ValueError("An immediate mode operand cannot be written to!")
        def register():
            if self._register < 0:
                if self._register == Registers.SP:
                    cpu.SP = value
                else:
                    cpu.PC = value
            else:
                cpu.set_register(value, self._register, self.width)
        def register_post():
            new_value = value + 1 if self._mode == Addressing.RegisterIncrement else value - 1
            if self._register < 0:
                if self._register == Registers.SP:
                    cpu.SP = new_value
                else:
                    cpu.PC = new_value
            else:
                cpu.set_register(new_value, self._register, self.width)
        def reg_indirect():
            mem_bus.WriteWorkRAM(register(), value)
        def direct():
            mem_bus.WriteWorkRAM(location, value)
        def indirect():
            indirect_loc = mem_bus.ReadWorkRAM(location, self.width)
            return mem_bus.ReadWorkRAM(indirect_loc, self.width)

        value_map = {
            Addressing.Immediate: immediate,
            Addressing.Register: register,
            Addressing.RegisterIncrement: register_post,
            Addressing.RegisterDecrement: register_post,
            Addressing.RegisterPlusImmediate: immediate,
            Addressing.RegisterIndirect: reg_indirect,
            Addressing.Direct: direct,
            Addressing.Indirect: indirect}

        value_map[self._mode]()
    #end set_value

    def ToString(self, mem_bus, address):
        """
        Returns a string that can be better read alongside similar strings for reading
        """
        # Returns something like "A", "(BC)", "imm"
        if self._mode != Addressing.Direct and self._mode != Addressing.Immediate:
            return self.__str__()

        formatter = "0x{0:02X}" if self.width == 1 else "0x{0:04X}"
        val = int.from_bytes(mem_bus.ReadWorkRAM(address, self.width), 'big')
        base = formatter.format(val)
        return base if self._mode == Addressing.Immediate else ("(%s) => %s" % base, int.from_bytes(mem_bus.ReadWorkRAM(val, self.width), 'big'))
    #end

    def __eq__(self, other):
        # Two operands are equal if they are operating on registers with the same mode and have the same width
        # We can't say memory operands are equal without binding to the address
        return self._mode == other._mode and\
             (self._mode != Addressing.Immediate and self._mode != Addressing.Direct)\
                  and self.width == other.width and self._register == other._register


    def __str__(self):
        """
        String that describes the operand.
        Returns something like "A", "(BC)", "imm"
        """
        if self._mode == Addressing.Immediate:
            return "imm"
        elif self._mode == Addressing.Register:
            return GetRegisterName(self._register, self.width)
        elif self._mode == Addressing.RegisterIndirect:
            return "(%s)" % GetRegisterName(self._register, self.width)
        elif self._mode == Addressing.Direct:
            return "(addr)"

        return "Unsupported addressing mode operand"
    #end

    def __repr__(self):
        """
        Debugging representation of the operand
        Returns something like
        "<Operand '(HL)' at 0x7f0ff7d6b100>"
        """
        return "<Operand '{0}' at {1}>".format(
            str(self),
            hex(id(self))
        )
    #end
#end operand

class Instruction:
    """
    Internal representation of an LR35902 instruction.
    Contains lots of debugging info/metadata (mnemonic, opcode) but also has
    all of the info needed to execute when combined with the current location, the CPU and the memory bus
    """

    def __init__(self, opcode, shorthand, bus_width, byte_size, cycles, flags, operands = (None,None), executor = None, store = None):
        self._opcode = opcode
        self._mnemonic = shorthand
        self._result_size = bus_width
        self._size = byte_size
        self._cycles = cycles
        self._flags_affected = flags

        # TODO: in the interest of building something quick, we'll allow this to always be None by default
        self._action = executor
        self._operands = operands
        #self._writeback = store
    #end

    def _get_operands(self, cpu, mem_bus, location):
        if self._operands is None:
            return (None, None)

        dest_op, src_op = self._operands
        dest = None if dest_op is None else dest_op.get_value(cpu, mem_bus, location)
        src = None if src_op is None else src_op.get_value(cpu, mem_bus, location)
        return (dest, src)

    def _set_flags(self, cpu, raw_result, result, destination, source):
        """Internally sets the CPU flags """

        # Short circuit if this instruction never sets any flags
        if self._flags_affected is None:
            return

        # Methods that will get the result
        def zero():
            return result == 0
        def negative():
            # TODO: check if correct
            return result < 0
        def half_carry():
            # Really good explanation behind the Half-Carry flag
            # https://robdor.com/2016/08/10/gameboy-emulator-half-carry-flag/
            return (((destination & 0xF) + (source & 0xF)) & 0x10) == 0x10
        def carry():
            return raw_result > result

        # We use a dictionary in case we have instructions where directly executing the above methods would be an exception
        # For example, in the INC instruction, running half_carry would throw unsupported operand exception if source is None
        results = {Flag.z: zero, Flag.n: negative, Flag.h: half_carry, Flag.c: carry}

        for flag, status in self._flags_affected.items():
            if status is Bit.Calculate:
                cpu.set_flag(results[flag](), flag)
            elif status is not None:
                cpu.set_flag(status == Bit.Set, flag)
        #end for
    #end set_flags

    def execute(self, cpu, mem_bus, location):
        """ Runs the instruction action on the known operands and returns the result """
        # quick check
        if self._action is None:
            return None

        #Get the operands
        dest, source = self._get_operands(cpu, mem_bus, location)

        # Do the thing and box the result!
        raw_result = self._action(cpu, dest, source)
        result = (raw_result & 0xFF) if self._result_size == 1 else (raw_result & 0xFFFF)

        # Check the flag status
        self._set_flags(cpu, raw_result, result, dest, source)

        return result
    #end execute

    def writeback(self, cpu, mem_bus, location, result):
        if self._operands is None or self._operands[0] is None:
            # write back would be illegal
            return

        self._operands[0].set_value(cpu, mem_bus, location, result)
    #end writeback

    @property
    def Opcode(self):
        """ The instruction op-code """
        return self._opcode

    @property
    def Mnemonic(self):
        """ Readable shorthand of the instruction """
        return self._get_mnemonic()

    @property
    def Length(self):
        """ Gets the length of the instruction in bytes """
        return self._size

    def is_complete(self):
        return self._action is not None

    def _get_mnemonic(self, mem_bus = None, addr = None):
        if self._operands is None:
            return self._mnemonic

        fmt = self._mnemonic.split(' ')
        base = fmt[0]
        src = dst = None
        if self._operands[0] is not None:
            dst = str(self._operands[0]) if mem_bus is None else self._operands[0].ToString(mem_bus, addr)
        if self._operands[1] is not None:
            src = str(self._operands[1]) if mem_bus is None else self._operands[1].ToString(mem_bus, addr)

        # TODO: handle mnemonics like "DEC C", "POP BC"
        return "{} {}".format(base, dst) if dst == src else "{} {},{}".format(base, dst, src)

    def ToString(self, mem_bus, address):
        """
        Returns a string that can be better read alongside similar strings for reading
        """
        # Returns something like
        # "0x0D  LD SP,d16      2byte, 4cycle"
        return "0x{0:04X} 0x{1:<8X}   {2:12}".format(
            address,
            self._opcode,
            self._get_mnemonic(mem_bus, address)
        )

    def __str__(self):
        """
        String that describes the CPU instruction
        Returns something like
        "0x0D  LD SP,d16      2byte, 4cycle"
        """
        return "0x{0:02X}   {1:12} {2}byte, {3}cycle".format(
            self._opcode,
            self._get_mnemonic(),
            self._size,
            self._cycles
        )

    def __repr__(self):
        """
        Debugging representation of the instruction
        Returns something like
        "<Instruction 0x31 'LD SP,d16' at 0x7f0ff7d6b100>"
        """
        return "<Instruction 0x{0:02X} '{1}' at {2}>".format(
            self._opcode,
            self._get_mnemonic(),
            hex(id(self))
        )
# end Instruction class

# HACK: the generators below work, but are not the best to use
#       for now, let's make sure the instructions work
#       and then ideally we can make an Operands class that knows how to Get/Set
#       that would also allow us to eliminate the need for an explicit "writeback" method

def gen_cpu_operand(reg):
    def gen(size, cpu, mem_bus, location):
        return cpu.get_register(reg, size)
    return gen

def gen_immediate_operand():
    def gen(size, cpu, mem_bus, location):
        return mem_bus.ReadWorkRAM(location, size)
    return gen

def gen_memory_operand(reg=None):
    def gen(size, cpu, mem_bus, location):
        mem_address = cpu.get_register(reg) if reg is not None else mem_bus.ReadWorkRAM(location, size)
        return mem_bus.ReadWorkRAM(mem_address, size)
    return gen

def gen_cpu_callback(reg):
    if type(reg) is str:
        if reg == 'SP':
            def gen(size, cpu, mem_bus, result):
                cpu.SP = result
            return gen
        elif reg == 'PC':
            def gen(size, cpu, mem_bus, result):
                cpu.PC = result
            return gen
    else:
        def gen(size, cpu, mem_bus, result):
            cpu.set_register(result, reg, size)
    return gen

def gen_mem_callback(addr):
    def gen(size, cpu, mem_bus, result):
        mem_bus.WriteWorkRAM(addr, result)
    return gen

# High-level logic for instructions is implemented below.
# Where applicable, comments have been added for clarity
# See http://z80-heaven.wikidot.com/ for more detailed info

def NoOp(cpu, destination, source):
    return None
def Reset(cpu, destination, source):
    return 0
#end

def InvalidInstruction(cpu, destination, source):
    raise SystemError()
def NotImplementedYet(cpu, destination, source):
    raise NotImplementedError()
#end

import operator

def _from_operator(an_operator):
    def func(cpu, destination, source):
        return an_operator(destination, source)
    return func
#end

Add = _from_operator(operator.add)
def AddWithCarry(cpu, destination, source):
    return Add(cpu, destination, source) + CPU.c
#end

Subtract = _from_operator(operator.sub)
Compare = Subtract
def SubWithCarry(cpu, destination, source):
    return Subtract(cpu, destination, source + CPU.c)
#end

BinOr = _from_operator(operator.or_)
BinXor = _from_operator(operator.xor)
BinAnd = _from_operator(operator.and_)

def Increment(cpu, destination, source):
    return source + 1
def Decrement(cpu, destination, source):
    return source - 1
#end

def RotateLeft(cpu, destination, source):
    """ From z80 Heaven:
    9-bit rotation to the left, the register's bits are shifted left.
    The carry value is put into 0th bit of the register, and the leaving 7th bit is put into the carry.
    """
    # Note: in our implementation Carry is set if the 9th bit (bit 8) is set
    return (source << 1) | cpu.C
def RotateLeftWithCarry(cpu, destination, source):
    """ From z80 Heaven:
    8-bit rotation to the left. The bit leaving on the left is copied into the carry, and to bit 0.
    """
    return (source << 1) | (source >> 7)
#end

def RotateRight(cpu, destination, source):
    """ From z80 Heaven:
    9-bit rotation to the right.
    The carry is copied into bit 7, and the bit leaving on the right is copied into the carry.
    """
    # Note: in our implementation Carry is set if the 9th bit is set. This Instruction happens as follows
    # [section A] | [section B] | [section C]
    # A: Shift source right by 1 (the actual operation)
    # B: Move the least signifcant bit up to the bit 8. This will ensure to set/reset the carry bit later in Instructions._set_flags method
    # C: Put the carry bit in bit 7
    return (source >> 1) | ((source & 1) << 8) | (cpu.C << 7)
def RotateRightWithCarry(cpu, destination, source):
    """ From z80 Heaven:
    8-bit rotation to the right. the bit leaving on the right is copied into the carry, and into bit 7.
    """
    # Fairly similar to above, but note that the LSB is copied both to bit 7 and 8 (carry set/reset)
    return (source >> 1) | ((source & 1) << 8) | ((source & 1) << 7)
#end

def Load(cpu, destination, source):
    # Just return the source, what matters for this one is the Write callback onto destination
    return source
#end

# TODO: implement rest of instructions (JP, Call, Push, Pop)
def InstructionPrototype(cpu, destination, source):
    pass
#end
