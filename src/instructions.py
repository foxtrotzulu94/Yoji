from .cpu_types import *

class Instruction:
    def __init__(self, opcode, shorthand, bus_width, byte_size, cycles, flags, executor):
        self._opcode = opcode
        self._mnemonic = shorthand
        self._result_size = bus_width
        self._size = byte_size
        self._cycles = cycles
        self._flags_affected = flags
        self._action = executor
    #end

    @property
    def Opcode(self):
        """ The instruction op-code """
        return self._opcode

    @property
    def Mnemonic(self):
        """ Readable shorthand of the instruction """
        return self._mnemonic

    def __str__(self):
        # Returns something like
        # "0x0D  DEC C      2byte, 4cycle"
        return "0x{0:02X}   {1:12} {2}byte, {3}cycle".format(
            self._opcode,
            self._mnemonic,
            self._size,
            self._cycles
        )

    def __repr__(self):
        # Returns something like
        # "<Instruction 0x31 'LD SP,d16' at 0x7f0ff7d6b100>"
        return "<Instruction 0x{0:02X} '{1}' at {2}>".format(
            self._opcode,
            self._mnemonic,
            hex(id(self))
        )

    def execute(cpu, set_callback, dest, source):
        # Run the instruction
        result = self.action(set_callback, result_size, dest, source)

        # Check if it set any flags
        # TODO
# end

def Load(dest_callback, dest, source):
    pass

def Add(cpu, width, destination, source):
    result = source + destination
    boxed_result = (result & 0xFF) if width == 1 else (result & 0xFFFF)
    destination = result

    # set the flags
    cpu.Z = (boxed_result == 0)
    cpu.N = 0

    # Really good explanation behind the Half-Carry flag
    # https://robdor.com/2016/08/10/gameboy-emulator-half-carry-flag/
    cpu.H = (((destination & 0xF) + (source & 0xF)) & 0x10) == 0x10
    cpu.C = result > boxed_result

known_instructions = [
    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={'z':None, 'n': None, 'h':None, 'c':None},
        executor = None),

    Instruction(
        0x31, "LD SP,d16", bus_width=2,
        byte_size=2, cycles=13,
        flags={'z':None, 'n': None, 'h':None, 'c':None},
        # TODO!
        executor = lambda x: 0),

    Instruction(
        0x81, "ADD A,C", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: Bit.Calculate, Flag.n: Bit.Unset, Flag.h:Bit.Calculate, Flag.c: Bit.Calculate},
        executor = lambda x: 0),
]

opcode_map = { x.Opcode: x for x in known_instructions }
