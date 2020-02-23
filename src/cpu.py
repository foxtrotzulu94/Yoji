from .cpu_types import *
from .instructions import Instruction, known_instructions

class CPU:
    """
    Emulates the Sharp LR35902 by instruction interpretation
    """

    def __init__(self, mem_bus):
        self.__program_counter = 0
        self.__stack_ptr = 0
        self.__registers = bytearray(2 * 4)

        self.__memory_bus = mem_bus

        # Technically, we can just use array indices to find it since known_instructions should be implemented as an ordered list
        # but we haven't really implemented the CB prefixes and this makes it easier to detect what opcodes we're missing since we'd get a KeyError
        #
        self.__opcode_map = { x.Opcode: x for x in known_instructions }
    # end init

    ### Bit Flag methods ###
    def __get_flag(self, bit_offset):
        return (self.__registers[1] & (1 << bit_offset)) == (1 << bit_offset)

    def __set_flag(self, value, bit_offset):
        if value:
            self.__registers[1] = self.__registers[1] | 1 << bit_offset
        else:
            self.__registers[1] = (self.__registers[1] & ~(1 << bit_offset))

    def _generate_get_flag(bit_offset):
        def gen(self):
            return self.__get_flag(bit_offset)
        return gen

    def _generate_set_flag(bit_offset):
        def gen(self, value):
            return self.__set_flag(value, bit_offset)
        return gen

    ### Register Flag methods ###
    def __get_register(self, offset, length):
        return self.__registers[offset : offset+length]

    def __set_register(self, value, offset, length):
        if type(value) is int:
            value = bytearray(value.to_bytes(length, 'big'))
        self.__registers[offset : offset+length] = value

    def _generate_get_register(offset, length = 1):
        def gen(self):
            return self.__get_register(offset, length)
        return gen

    def _generate_set_register(offset, length = 1):
        def gen(self, value):
            return self.__set_register(value, offset, length)
        return gen

    ### Properties ###

    @property
    def PC(self):
        """ The 16-bit Program Counter """
        return self.__program_counter

    @PC.setter
    def PC(self, value):
        self.__program_counter = value

    @property
    def SP(self):
        """ The 16-bit Stack Pointer """
        return self.__stack_ptr

    @SP.setter
    def F(self, value):
        self.__stack_ptr = value

    ## Registers ##
    # 8-BIT WIDTH #
    A = property(_generate_get_register(Registers.A), _generate_set_register(Registers.A), None, "The 8-bit Accumulator register")
    F = property(_generate_get_register(Registers.F), _generate_set_register(Registers.F), None, "The Flag register")
    B = property(_generate_get_register(Registers.B), _generate_set_register(Registers.B), None, "General purpose 8-bit register")
    C = property(_generate_get_register(Registers.C), _generate_set_register(Registers.C), None, "General purpose 8-bit register")
    D = property(_generate_get_register(Registers.D), _generate_set_register(Registers.D), None, "General purpose 8-bit register")
    E = property(_generate_get_register(Registers.E), _generate_set_register(Registers.E), None, "General purpose 8-bit register")
    H = property(_generate_get_register(Registers.H), _generate_set_register(Registers.H), None, "General purpose 8-bit register")
    L = property(_generate_get_register(Registers.L), _generate_set_register(Registers.L), None, "General purpose 8-bit register")

    # 16-BIT WIDTH #
    BC = property(_generate_get_register(Registers.B,2), _generate_set_register(Registers.B,2), None, "General purpose 16-bit register")
    DE = property(_generate_get_register(Registers.C,2), _generate_set_register(Registers.D,2), None, "General purpose 16-bit register")
    HL = property(_generate_get_register(Registers.H,2), _generate_set_register(Registers.H,2), None, "General purpose 16-bit register")

    ## Flags ##
    z = property(_generate_get_flag(Flag.z), _generate_set_flag(Flag.z), None, "The Zero bit flag")
    n = property(_generate_get_flag(Flag.n), _generate_set_flag(Flag.n), None, "The Subtract bit flag")
    h = property(_generate_get_flag(Flag.h), _generate_set_flag(Flag.h), None, "The Half Carry bit flag")
    c = property(_generate_get_flag(Flag.c), _generate_set_flag(Flag.c), None, "The Carry bit flag")

    # TODO: Instructions

    # TODO: Tick method

    def Dump(self, move_forward = True):
        "Dumps the current CPU instruction about to be executed"

        # Instruction Fetch
        opcode = self.__memory_bus.ReadWorkRAM(self.PC, 1)

        # Decode and dump
        instruction = self.__opcode_map[int.from_bytes(opcode, 'big')]
        print(instruction.ToString(self.PC))

        if move_forward:
            self.PC += instruction.Length + 1
    #end dump