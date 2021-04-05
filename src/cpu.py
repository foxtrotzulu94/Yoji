from typing import *

from .cpu_types import Registers, Flag
from .bus import InterruptBit
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
        self._next_instr_cycle = 0

        self.__base_opcodes = base_instructions
        self.__cb_opcodes = cb_prefix

        self.__debug = False
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
    def Debug(self):
        """ Debug mode to print instructions on each tick """
        return self.__debug

    @Debug.setter
    def Debug(self, value):
        self.__debug = value

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
    AF = property(_generate_get_register(Registers.A,2), _generate_set_register(Registers.A,2), None, "General purpose 16-bit register")
    BC = property(_generate_get_register(Registers.B,2), _generate_set_register(Registers.B,2), None, "General purpose 16-bit register")
    DE = property(_generate_get_register(Registers.D,2), _generate_set_register(Registers.D,2), None, "General purpose 16-bit register")
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

    InterruptJumpTable = {
        InterruptBit.VBlank: 0x40,
        InterruptBit.LCD_STAT: 0x48,
        InterruptBit.Timer: 0x50,
        InterruptBit.Serial: 0x58,
        InterruptBit.Joypad: 0x60,
    }

    def _execute_instruction(self, location):
        self._curr_result = self._curr_inst.execute(self, self.__memory, location)
    def _check_interrupts(self):
        if not self.__interrupts_enabled:
            return

        raised = self.__memory.CheckInterruptFlags()
        if raised == 0:
            return

        enabled = self.__memory.CheckInterruptEnable()
        for bit in InterruptBit:
            if (enabled & bit) == bit and (raised & bit) == bit:
                # If we were suspended, wake up!
                self.__suspended = False

                # Turn the bit off and Go handle the interrupt
                self.__memory.SetInterruptFlags(bit, False)
                self.__interrupts_enabled = False
                self.PushStack(self.PC)
                self.PC = CPU.InterruptJumpTable[bit]

                # The interrupt routine will proceed to execute as normal
                return
            #end if
        #end for
    #end

    def Step(self):
        "Executes the next instruction immediately"

        self._check_interrupts()
        if self.__suspended:
            return

        # 1. Instruction Fetch, Decode
        self._get_next_instruction()
        location = self.PC

        self.PC += self._curr_inst.Size
        nextPC = self.PC

        # 2. Execute & Writeback
        self._execute_instruction(location + 1)
    #end Step

    def Tick(self, cycle_num):
        "Executes instructions to the tick of a clock"

        if cycle_num < self._next_instr_cycle:
            return

        self._check_interrupts()
        if self.__suspended:
            return

        # 1. Instruction Fetch, Decode
        self._get_next_instruction()
        location = self.PC

        self.PC += self._curr_inst.Size
        nextPC = self.PC

        # 2. Execute & Writeback
        # if self.__debug:
        #     print(self._curr_inst.ToString(self.__memory, location))
        # TODO: Verify this location + 1
        self._execute_instruction(location + 1)

        # Check how many cycles we have left for the next instruction
        if self.PC == nextPC and self._curr_inst.ShortCycles is not None:
            # This means we didn't take the Jump, so there's no memory penalty to pay here
            self._next_instr_cycle = cycle_num + self._curr_inst.ShortCycles# - 1
        else:
            self._next_instr_cycle = cycle_num + self._curr_inst.Cycles# - 1
    #end Tick
#end class
