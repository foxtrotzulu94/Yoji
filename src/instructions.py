from .cpu_types import *
from .operands import Operand, Addressing

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

    def _get_operand(self, index, cpu, mem, location):
        if self._operands is None or self._operands[index] is None:
            return None
        val = self._operands[index].get_value(cpu, mem, location)
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

    def execute(self, cpu, mem, location):
        """ Runs the instruction action on the known operands and returns the result """
        #Get the operands
        dest = self._get_operand(0, cpu, mem, location)
        source = self._get_operand(1, cpu, mem, location)

        # Do the thing and box the result!
        raw_result = self._action(cpu, dest, source)
        if raw_result is None:
            raw_result = 0
        result = (raw_result & 0xFF) if self._result_size == 1 else (raw_result & 0xFFFF)

        # Check the flag status
        self._set_flags(cpu, raw_result, result, dest, source)

        # Do writeback
        self.writeback(cpu, mem, location, result)

        return result
    #end execute

    def writeback(self, cpu, mem, location, result):
        if self._operands is None or self._operands[0] is None:
            # write back would be illegal
            return

        self._operands[0].set_value(cpu, mem, location, result)
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

    def _get_mnemonic(self, mem = None, addr = None):
        if self._operands is None:
            return self._mnemonic

        fmt = self._mnemonic.split(' ')
        base = fmt[0]
        src = dst = None
        if self._operands[0] is not None:
            dst = str(self._operands[0]) if mem is None else self._operands[0].ToString(mem, addr)
        if self._operands[1] is not None:
            src = str(self._operands[1]) if mem is None else self._operands[1].ToString(mem, addr)

        return "{} {}".format(base, src) if dst == src or dst is None else "{} {},{}".format(base, dst, src)

    def ToString(self, mem, address):
        """
        Returns a string that can be better read alongside similar strings for reading
        """
        # Returns something like
        # "0x0D  LD SP,d16      2byte, 4cycle"
        return "0x{0:04X}    0x{1:<4X}   {2:12}".format(
            address,
            self._opcode,
            self._get_mnemonic(mem, address+1)
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

def ShiftLeft(_, unused, source):
    # Note: in our implementation Carry is set if the 9th bit (bit 8) is set
    return source << 1
def RotateLeft(cpu, unused, source):
    """ From z80 Heaven:
    9-bit rotation to the left, the register's bits are shifted left.
    The carry value is put into 0th bit of the register, and the leaving 7th bit is put into the carry.
    """
    return (source << 1) | cpu.C
def RotateLeftWithCarry(cpu, unused, source):
    """ From z80 Heaven:
    8-bit rotation to the left. The bit leaving on the left is copied into the carry, and to bit 0.
    """
    return (source << 1) | (source >> 7)
#end

def ShiftRight(cpu, unused, source):
    # Note: in our implementation Carry is set if the 9th bit is set.
    # We need to shift right, and place bit 0 in the carry
    return (source >> 1) | ((source & 1) << 8)
def ShiftRightArithmetic(cpu, unused, source):
    # Do the above, but preserving bit 7
    return (source >> 1) | ((source & 1) << 8) | (source & 0x40)
def RotateRight(cpu, unused, source):
    """ From z80 Heaven:
    9-bit rotation to the right.
    The carry is copied into bit 7, and the bit leaving on the right is copied into the carry.
    """
    # This Instruction happens as follows
    # [section A] | [section B] | [section C]
    # A: Shift source right by 1 (the actual operation)
    # B: Move the least signifcant bit up to the bit 8. This will ensure to set/reset the carry bit later in Instructions._set_flags method
    # C: Put the carry bit in bit 7
    return (source >> 1) | ((source & 1) << 8) | (cpu.c << 7)
def RotateRightWithCarry(cpu, unused, source):
    """ From z80 Heaven:
    8-bit rotation to the right. the bit leaving on the right is copied into the carry, and into bit 7.
    """
    # Fairly similar to above, but note that bit 0 is copied both to bit 7 and 8 (carry set/reset)
    return (source >> 1) | ((source & 1) << 8) | ((source & 1) << 7)
#end

def Load(cpu, unused, source):
    # Just return the source, what matters for this one is the Write callback onto destination
    return source
def Swap(_, __, source):
    hi = source & 0xF0
    lo = source & 0xF
    result = (lo << 4) | (hi >> 4)
    return result
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

def Push(cpu, unused, val):
    cpu.PushStack(val)
    return 0
def Pop(cpu, *unused):
    return cpu.PopStack()
def Call(cpu, condition, location):
    # Call into a routine.
    # Note that None is not False
    if condition is False:
        return

    # The PC is always pointing at the next instruction now
    Push(cpu, None, cpu.PC)
    cpu.PC = location
def Return(cpu, condition, unused):
    if condition is False:
        return

    cpu.PC = Pop(cpu, None)
def ReturnInterrupt(cpu, *unused):
    Return(cpu, None, None)
    EnableInterrupts(cpu)
def Restart(cpu, unused, source):
    # Calls into the GameBoy's Restart and Interrupt vector location
    Push(cpu, None, cpu.PC +3)
    cpu.PC = source & 0x00FF
def Halt(cpu, *unused):
    cpu.Halt()
Stop = Halt # TODO? We might need to do blank the screen
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

def EnableInterrupts(cpu, *unused):
    cpu.EnableInterrupts(True)
def DisableInterrupts(cpu, *unused):
    cpu.EnableInterrupts(False)
#end

def ComplementA(cpu, *unused):
    # Fairly specific
    cpu.A = (cpu.A ^ 0xFF) & 0xFF
    return cpu.A
def DecimalAdjustAccumulator(cpu, *unused):
    """ From z80 heaven:
    When this instruction is executed, the A register is BCD corrected using the contents of the flags.
    """
    # The exact process is the following:
    # if the least significant four bits of A contain a non-BCD digit (i. e. it is greater than 9) or the H flag is set,
    # then $06 is added to the register. Then the four most significant bits are checked.
    # If this more significant digit also happens to be greater than 9 or the C flag is set, then $60 is added.
    if cpu.h or (cpu.A & 0xF) > 9:
        cpu.A += 0x6

    if cpu.c or ((cpu.A & 0xF0) >> 4) > 9:
        cpu.A += 0x60

    return cpu.A
#end
