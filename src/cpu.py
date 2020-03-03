from typing import *
from .cpu_types import Registers, Flag
from .memory import Memory
from .instructions import Instruction
from .base_instructions import base_instructions
from .cb_prefix_instructions import cb_prefix

class CPU:
    """
    Emulates the Sharp LR35902 by instruction interpretation
    """

    def __init__(self, memory: Memory):
        self.__program_counter = 0
        self.__stack_ptr = 0
        self.__stack_size = 0
        self.__registers = bytearray(2 * 4)

        self.__memory = memory
        self.__interrupts_enabled = True
        self.__suspended = False

        self._curr_inst = None
        self._curr_result = None
        self._cycles_left = -1

        self.__base_opcodes = base_instructions
        self.__cb_opcodes = cb_prefix
    # end init

    ### Bit Flag methods ###
    def get_flag(self, bit_offset: int) -> bool:
        return (self.__registers[1] & (1 << bit_offset)) == (1 << bit_offset)

    def set_flag(self, value : bool, bit_offset: int):
        if value:
            self.__registers[1] = self.__registers[1] | 1 << bit_offset
        else:
            self.__registers[1] = (self.__registers[1] & ~(1 << bit_offset))

    def _generate_get_flag(bit_offset: int) -> Callable[['CPU'], bool]:
        def gen(self: 'CPU') -> bool:
            return self.get_flag(bit_offset)
        return gen

    def _generate_set_flag(bit_offset: int) -> Callable[['CPU', bool], None]:
        def gen(self: 'CPU', value: bool):
            self.set_flag(value, bit_offset)
        return gen

    ### Register Flag methods ###
    # NOTE they use big endian because the MSB should be stored in the first 8-bit register!
    def get_register(self, offset: int, length: int) -> int:
        """ Get method for regular registers """
        return int.from_bytes(self.__registers[offset : offset+length], 'big')

    def set_register(self, value : int, offset: int, length: int):
        """ Set method for regular registers """
        data = bytes()
        if type(value) is int:
            data = bytes([value]) if length == 1 else bytes([ (value&0xFF00) >> 8, value & 0xFF] )
        for i in range(0, length):
            self.__registers[offset + i] = data[i]

    def _generate_get_register(offset: int, length: int = 1) -> Callable[['CPU'], int]:
        def gen(self: 'CPU') -> int:
            return self.get_register(offset, length)
        return gen

    def _generate_set_register(offset: int, length: int = 1) -> Callable[['CPU', int], None]:
        def gen(self: 'CPU', value: int):
            self.set_register(value, offset, length)
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
    def SP(self, value):
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

    def EnableInterrupts(self, is_enabled):
        self.__interrupts_enabled = is_enabled
    def Halt(self):
        self.__suspended = True
    #end

    # HACK: The stack operations need access to memory
    # Right now, the way this fits in the instruction machinery makes it complicated and wrong
    # but when executing instructions, we have a handle back to the CPU, so just use it here directly.
    def PushStack(self, value):
        converted = value.to_bytes(2, 'little')
        self.SP -= 2
        self.__memory.Write(self.SP, converted)
        self.__stack_size += 1
    def PeekStack(self):
        if self.__stack_size == 0:
            return 0

        return self.__memory.Read(self.SP, 2)
    def PopStack(self):
        assert(self.__stack_size > 0)
        top = self.PeekStack()
        self.SP += 2
        self.__stack_size -= 1
        return int.from_bytes(top, 'little')
    #end

    def _get_next_instruction(self):
        opcode = self.__memory.Read(self.PC)[0]
        instr = self.__base_opcodes[opcode]
        if opcode == 0xCB:
            opcode = self.__memory.Read(self.PC+1)[0]
            instr = self.__cb_opcodes[opcode]

        self._curr_inst = instr
    #end

    def _execute_instruction(self, location):
        self._curr_result = self._curr_inst.execute(self, self.__memory, location)
    def _check_interrupts(self):
        if not self.__interrupts_enabled:
            return

        # TODO: Check for pending interrupts to handle at mem 0xFF0F

        # TODO: When an interrupt is available, before dealing with it, set
        self.__suspended = False
    #end

    def Step(self):
        "Executes the next instruction immediately"

        # Instruction Fetch, Decode is handled in Dump
        self.Dump(False)

        if not self.__suspended:
            # execute
            location = self.PC + 1
            self.PC += self._curr_inst.Size
            self._execute_instruction(location)
        #end

        self._check_interrupts()
    #end Step

    def Tick(self):
        "Executes instructions to the tick of a clock"

        self._cycles_left = max(self._cycles_left - 1, 0)
        if self._cycles_left > 0:
            return

        self._check_interrupts()
        if self.__suspended:
            return

        self._get_next_instruction() # 1. Instruction Fetch, Decode
        self.PC += self._curr_inst.Size
        self._execute_instruction()  # 2. Execute & Writeback

        self._cycles_left = self._curr_inst.Cycles - 1
    #end Tick

    def Dump(self, move_forward = True):
        "Dumps the current CPU instruction about to be executed"

        # Fetch, Decode and dump
        self._get_next_instruction()
        print(self._curr_inst.ToString(self.__memory, self.PC))

        if move_forward:
            self.PC += max(self._curr_inst.Size, 1)
    #end dump

    def executeArbitraryInstruction(self, opcode):
        """ solely for debugging purposes """
        instr = None

        # Instruction decode
        if type(opcode) is int:
            instr = self.__opcode_map[opcode]
            if (opcode & 0xFF00) == 0xCB00:
                opcode = (opcode >> 8)
                instr = self.__opcode_map[0xcb][opcode]
        elif type(opcode) is str:
            # This is pretty darn slow...
            matching = [ x for x in base_instructions + cb_prefix if x._mnemonic == opcode ]
            if len(matching) < 1:
                raise KeyError("Mnemonic not found!")
            instr = matching[0]
        #end

        # Instruction Execute
        location = self.PC + 1
        print(instr.ToString(self.__memory, self.PC))
        result = instr.execute(self, self.__memory, location)

        # Writeback
        instr.writeback(self, self.__memory, location, result)
        self._check_interrupts()
    #end
#end class
