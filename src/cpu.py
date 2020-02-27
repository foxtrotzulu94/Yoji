from .cpu_types import *
from .instructions import Instruction
from .known_instructions import known_instructions, cb_prefix

class CPU:
    """
    Emulates the Sharp LR35902 by instruction interpretation
    """

    def __init__(self, mem_bus):
        self.__program_counter = 0
        self.__stack_ptr = 0
        self.__stack_size = 0
        self.__registers = bytearray(2 * 4)

        self.__memory_bus = mem_bus

        self._curr_inst = None
        self._curr_result = None
        self._cycles_left = -1

        # Technically, we can just use array indices to find it since known_instructions should be implemented as an ordered list
        self.__opcode_map = { x.Opcode: x for x in known_instructions }
        self.__opcode_map[0xCB] = { x.Opcode: x for x in cb_prefix }
    # end init

    ### Bit Flag methods ###
    def get_flag(self, bit_offset):
        return (self.__registers[1] & (1 << bit_offset)) == (1 << bit_offset)

    def set_flag(self, value, bit_offset):
        if value:
            self.__registers[1] = self.__registers[1] | 1 << bit_offset
        else:
            self.__registers[1] = (self.__registers[1] & ~(1 << bit_offset))

    def _generate_get_flag(bit_offset):
        def gen(self):
            return self.get_flag(bit_offset)
        return gen

    def _generate_set_flag(bit_offset):
        def gen(self, value):
            return self.set_flag(value, bit_offset)
        return gen

    ### Register Flag methods ###
    def get_register(self, offset, length):
        """ Get method for regular registers """
        return self.__registers[offset : offset+length]

    def set_register(self, value, offset, length):
        """ Set method for regular registers """
        if type(value) is int:
            value = bytearray(value.to_bytes(length, 'little'))
        self.__registers[offset : offset+length] = value

    def _generate_get_register(offset, length = 1):
        def gen(self):
            return self.get_register(offset, length)
        return gen

    def _generate_set_register(offset, length = 1):
        def gen(self, value):
            return self.set_register(value, offset, length)
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

    # HACK: The stack operations need access to memory
    # Right now, the way this fits in the instruction machinery makes it complicated and wrong
    # but when executing instructions, we have a handle back to the CPU, so just use it here directly.
    def PushStack(self, value):
        self.__memory_bus.WriteWorkRAM(self.SP, value.to_bytes(2, 'little'))
        self.__stack_size += 1
        self.SP -= 2
    def PeekStack(self):
        if self.__stack_size == 0:
            return 0

        return self.__memory_bus.ReadWorkRAM(self.SP+2, 2)
    def PopStack(self):
        assert(self.__stack_size > 0)
        top = self.PeekStack()
        self.SP += 2
        self.__stack_size -= 1
        return int.from_bytes(top, 'little')
    #end


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

    def _get_next_instruction(self):
        opcode = self.__memory_bus.ReadWorkRAM(self.PC, 1)
        instr = self.__opcode_map[int.from_bytes(opcode, 'big')]
        if type(instr) is not Instruction:
            opcode = self.__memory_bus.ReadWorkRAM(self.PC+1, 1)
            instr = instr[int.from_bytes(opcode, 'big')]

        self._curr_inst = instr
    #end

    def _execute_instruction(self):
        location = self.PC + 1
        self._curr_result = self._curr_inst.execute(self, self.__memory_bus, location)
    #end

    def Step(self):
        "Executes the next instruction immediately"

        self.Dump(False)

        # Instruction Fetch, Decode
        self._get_next_instruction()

        # Instruction Execute
        location = self.PC + 1
        self._curr_result = self._curr_inst.execute(self, self.__memory_bus, location)

        # Writeback
        self._curr_inst.writeback(self, self.__memory_bus, location, self._curr_result)
        self.PC += self._curr_inst.Size
    #end Step

    def Tick(self):
        "Executes instructions to the tick of a clock"

        self._cycles_left -= 1
        if self._cycles_left > 0:
            return

        # 3. Writeback
        if self._cycles_left == 0 and self._curr_inst is not None:
            # If we have an instruction, do the writeback step in the last possible cycle
            # this is to avoid any weird timing issues w.r.t the Memory bus
            self._curr_inst.writeback(self, self.__memory_bus, self.PC + 1, self._curr_result)
            self.PC += self._curr_inst.Size

        self._get_next_instruction() # 1. Instruction Fetch, Decode
        self._execute_instruction()  # 2. Execute

        self._cycles_left = self._curr_inst.Cycles - 1
    #end Tick

    def Dump(self, move_forward = True):
        "Dumps the current CPU instruction about to be executed"

        # Fetch, Decode and dump
        self._get_next_instruction()
        print(self._curr_inst.ToString(self.__memory_bus, self.PC))

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
            matching = [ x for x in known_instructions+cb_prefix if x.Mnemonic == opcode ]
            if len(matching) < 1:
                raise KeyError("Mnemonic not found!")
            instr = matching[0]
        #end

        # Instruction Execute
        location = self.PC + 1
        print(instr.ToString(self.__memory_bus, self.PC))
        result = instr.execute(self, self.__memory_bus, location)

        # Writeback
        instr.writeback(self, self.__memory_bus, location, result)
    #end

