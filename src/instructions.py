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
        # Always used
        self._mode = addressing_mode
        self.width = width # 1 or 2 bytes

        # used when operands constants, bits, register enums
        self._register = reg
        self._throwaway = False

        # only used when bits are used to determine if we're checking set or reset bits
        # which is why we provide a default value
        self._bit_state = Bit.Ignore
    #end

    @staticmethod
    def bit(offset, state):
        op = Operand(offset, 1, Addressing.Bit)
        op._bit_state = state
        return op

    @staticmethod
    def const(value):
        return Operand(value, 1, Addressing.Constant)

    @staticmethod
    def reg(reg, width=1, throwaway = False):
        op = Operand(reg, width, Addressing.Register)
        op._throwaway = False
        return op

    @staticmethod
    def regi(reg, width=1):
        return Operand(reg, width, Addressing.RegisterIndirect)

    @staticmethod
    def regI(reg):
        return Operand(reg, 1, Addressing.RegisterPlusImmediate)

    @staticmethod
    def regInc(reg, width=1):
        return Operand(reg, width, Addressing.RegisterIncrement)

    @staticmethod
    def regDec(reg, width=1):
        return Operand(reg, width, Addressing.RegisterDecrement)

    @staticmethod
    def imm(width):
        return Operand(None, width, Addressing.Immediate)

    @staticmethod
    def mem(width):
        return Operand(None, width, Addressing.Direct)

    def can_set_value(self):
        """Checks if this operand can be used to set value"""
        return self._mode != Addressing.Immediate and self._mode != Addressing.RegisterPlusImmediate \
            and self._mode != Addressing.Bit and self._mode != Addressing.Constant

    def _get_register(self, cpu):
        if self._register < 0:
            return cpu.SP if self._register == Registers.SP else cpu.PC
        return cpu.get_register(self._register, self.width)

    def _translate_address(self, address):
        if self.width == 1:
            if type(address) is bytearray:
                address = address[0]
            address = address | 0xFF00
        return address

    def get_value(self, cpu, mem_bus, location):
        "Gets the value of the operand"

        # if we're retrieving a constant, just return immediately
        if self._mode == Addressing.Constant:
            return self._register

        # Methods that will get the value
        def bit():
            a_bit = cpu.get_flag(self._register)
            return a_bit if self._bit_state == Bit.Set else (not a_bit)
        def immediate():
            return mem_bus.ReadWorkRAM(location, self.width)
        def register():
            return self._get_register(cpu)
        def register_post():
            value = register()

            #Set the new value immediately
            new_value = value + 1 if self._mode == Addressing.RegisterIncrement else value - 1
            if self._register < 0:
                if self._register == Registers.SP:
                    cpu.SP = new_value
                else:
                    cpu.PC = new_value
            else:
                cpu.set_register(new_value, self._register, self.width)
            #end if-else

            return value
        def register_w_immediate():
            return register() + immediate()
        def reg_indirect():
            return mem_bus.ReadWorkRAM(self._translate_address(register()), self.width)
        def direct():
            return mem_bus.ReadWorkRAM(self._translate_address(immediate()), self.width)
        def indirect():
            return mem_bus.ReadWorkRAM(self._translate_address(direct()), self.width)

        value_map = {
            Addressing.Bit: bit,
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
            retVal = int.from_bytes(retVal, 'little')
        return retVal
    #end get_value

    def set_value(self, cpu, mem_bus, location, value):
        "Sets the value of the operand. Use for writeback step"

        # Throw exception now so we know
        if self._mode == Addressing.Immediate or self._mode == Addressing.RegisterPlusImmediate:
            raise ValueError("An immediate mode operand cannot be written to!")
        elif self._mode == Addressing.Constant:
            raise ValueError("A constant-value operand cannot be written to!")
        elif self._mode == Addressing.Bit:
            raise ValueError("A bit operand should not be written to directly!")

        # Methods that will get the value
        def register():
            if self._register < 0:
                if self._register == Registers.SP:
                    cpu.SP = value
                else:
                    cpu.PC = value
            else:
                cpu.set_register(value, self._register, self.width)
        def reg_indirect():
            wb_v = value
            if type(wb_v) is int:
                num_bytes = 1 if self._register != Registers.SP else 2
                wb_v = value.to_bytes(num_bytes, 'little')
            mem_bus.WriteWorkRAM(self._translate_address(self._get_register(cpu)), wb_v)
        def direct():
            mem_bus.WriteWorkRAM(self._translate_address(location), value)
        def indirect():
            indirect_loc = mem_bus.ReadWorkRAM(location, self.width)
            return mem_bus.ReadWorkRAM(self._translate_address(indirect_loc), self.width)

        value_map = {
            Addressing.Register: register,
            Addressing.RegisterIncrement: reg_indirect,
            Addressing.RegisterDecrement: reg_indirect,
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
        val = int.from_bytes(mem_bus.ReadWorkRAM(address, self.width), 'little')
        base = formatter.format(val)
        return base if self._mode == Addressing.Immediate else ("({})".format(base))
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
        elif self._mode == Addressing.RegisterDecrement or self._mode == Addressing.RegisterIncrement:
            symbol = '+' if self._mode == Addressing.RegisterIncrement else '-'
            return "({}{})".format(GetRegisterName(self._register, self.width), symbol)
        elif self._mode == Addressing.Direct:
            return "(addr)"
        elif self._mode == Addressing.Constant:
            return "{:X}H".format(self._register) if self._register > 7 else str(self._register)
        elif self._mode == Addressing.Bit:
            name = self._register.name.upper()
            return name if self._bit_state == Bit.Set else "N"+name

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

    def __init__(self, opcode, shorthand, bus_width, byte_size, cycles, flags, operands, executor):
        self._opcode = opcode
        self._mnemonic = shorthand
        self._result_size = bus_width
        self._size = byte_size
        self._cycles = cycles
        self._flags_affected = flags

        self._action = executor
        self._operands = operands
    #end

    def _get_operands(self, cpu, mem_bus, location):
        if self._operands is None:
            return (None, None)

        dest_op, src_op = self._operands
        dest = None if dest_op is None else dest_op.get_value(cpu, mem_bus, location)
        src = None if src_op is None else src_op.get_value(cpu, mem_bus, location)
        return (dest, src)
    #end

    def _get_operand(self, index, cpu, mem_bus, location):
        if self._operands is None or self._operands[index] is None:
            return None
        val = self._operands[index].get_value(cpu, mem_bus, location)
        if self._operands[index]._mode == Addressing.Bit:
            return val

        # this only works because of little-endian implementation, specifically:
        # if the lowest memory address was mapped to the LSB, then if we expect only 1 byte-width, but retrieved 2, we'll get the data address we expect
        return (val & 0xFF) if self._result_size == 1 else (val & 0xFFFF)
    #end

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
            raise NotImplementedError("The instruction is not implemented yet!\n\t{}".format(self.ToString(mem_bus, location-1)))
            return None

        #Get the operands
        get_operands = lambda idx: self._get_operand(idx, cpu, mem_bus, location)
        dest, source = get_operands(0), get_operands(1)

        # Do the thing and box the result!
        raw_result = self._action(cpu, dest, source)
        if raw_result is None:
            raw_result = 0
        result = (raw_result & 0xFF) if self._result_size == 1 else (raw_result & 0xFFFF)

        # Check the flag status
        self._set_flags(cpu, raw_result, result, dest, source)

        return result
    #end execute

    def writeback(self, cpu, mem_bus, location, result):
        if self._operands is None or self._operands[0] is None or not self._operands[0].can_set_value():
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
    def Size(self):
        """ Gets the length of the instruction in bytes """
        return self._size

    @property
    def Cycles(self):
        """ Gets the cycle count for the instruction """
        return self._cycles

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

        return "{} {}".format(base, src) if dst == src or dst is None else "{} {},{}".format(base, dst, src)

    def ToString(self, mem_bus, address):
        """
        Returns a string that can be better read alongside similar strings for reading
        """
        # Returns something like
        # "0x0D  LD SP,d16      2byte, 4cycle"
        return "0x{0:04X}    0x{1:<4X}   {2:12}".format(
            address,
            self._opcode,
            self._get_mnemonic(mem_bus, address+1)
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

# High-level logic for instructions is implemented below.
# Where applicable, comments have been added for clarity
# See http://z80-heaven.wikidot.com/ for more detailed info

def NoOp(*unused):
    return None
def Reset(*unused):
    return 0
#end

def InvalidInstruction(*unused):
    raise SystemError()
def NotImplementedYet(*unused):
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

def Increment(cpu, unused, source):
    return source + 1
def Decrement(cpu, unused, source):
    return source - 1
#end

def RotateLeft(cpu, unused, source):
    """ From z80 Heaven:
    9-bit rotation to the left, the register's bits are shifted left.
    The carry value is put into 0th bit of the register, and the leaving 7th bit is put into the carry.
    """
    # Note: in our implementation Carry is set if the 9th bit (bit 8) is set
    return (source << 1) | cpu.C
def RotateLeftWithCarry(cpu, unused, source):
    """ From z80 Heaven:
    8-bit rotation to the left. The bit leaving on the left is copied into the carry, and to bit 0.
    """
    return (source << 1) | (source >> 7)
#end

def RotateRight(cpu, unused, source):
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
def RotateRightWithCarry(cpu, unused, source):
    """ From z80 Heaven:
    8-bit rotation to the right. the bit leaving on the right is copied into the carry, and into bit 7.
    """
    # Fairly similar to above, but note that the LSB is copied both to bit 7 and 8 (carry set/reset)
    return (source >> 1) | ((source & 1) << 8) | ((source & 1) << 7)
#end

def Load(cpu, unused, source):
    # Just return the source, what matters for this one is the Write callback onto destination
    return source
#end

def CheckBit(_, bit, source):
    return (source & (1 << bit)) == 1 << bit
def SetBit(_, source, bit):
    return source | (1 << bit)
def SetCarry(cpu, *unused):
    # Carry is set in bit 8
    return 1 << 8
def InvertCarry(cpu,*unused):
    return 0 if cpu.c else SetCarry(cpu)
#end

def ComplementA(cpu, *unused):
    # Fairly specific
    cpu.A = (cpu.A ^ 0xFF) & 0xFF
    return cpu.A
def Push(cpu, unused, val):
    cpu.PushStack(val)
    return 0
def Pop(cpu, *unused):
    return cpu.PopStack()
#end

def Call(cpu, condition, location):
    # Call into a routine.
    # Note that None is not False
    if condition is False:
        return

    Push(cpu, None, cpu.PC + 3)
    cpu.PC = location
def Return(cpu, condition, unused):
    if condition is False:
        return

    cpu.PC = Pop(cpu, None)
ReturnInterrupt = Return # For now...
def Restart(cpu, unused, source):
    # Calls into the GameBoy's Restart and Interrupt vector location
    Push(cpu, None, cpu.PC +3)
    cpu.PC = source & 0xFF
#end

def Jump(cpu, condition, location):
    if condition is False:
        return
    cpu.PC = location
def NearJump(cpu, condition, signed_value):
    if condition is False:
        return

    value = signed_value
    if CheckBit(None, 7, signed_value):
        # Convert 2's complement back to integer and add a negative sign
        value = - (((~value)+1)&0xFF)

    cpu.PC = cpu.PC + value
#end


# TODO: implement rest of instructions (JP, Call, Push, Pop)
def InstructionPrototype(cpu, destination, source):
    pass
#end
