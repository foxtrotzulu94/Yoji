from .cpu_types import *

class Instruction:
    """
    Internal representation of an LR35902 instruction
    """
    
    def __init__(self, opcode, shorthand, bus_width, byte_size, cycles, flags, executor = None):
        self._opcode = opcode
        self._mnemonic = shorthand
        self._result_size = bus_width
        self._size = byte_size
        self._cycles = cycles
        self._flags_affected = flags

        # TODO: in the interest of building something quick, we'll allow this to always be None by default
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

    @property
    def Length(self):
        """ Gets the length of the instruction in bytes """
        return self._size

    def ToString(self, address):
        """
        Returns a string that can be better read alongside similar strings for reading
        """
        # Returns something like
        # "0x0D  DEC C      2byte, 4cycle"
        return "0x{0:04X} 0x{1:<8X}   {2:12}".format(
            address,
            self._opcode,
            self._mnemonic
        )

    def __str__(self):
        """
        String that describes the CPU instruction
        Returns something like
        "0x0D  DEC C      2byte, 4cycle"
        """
        return "0x{0:02X}   {1:12} {2}byte, {3}cycle".format(
            self._opcode,
            self._mnemonic,
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
#end

# The list below is every single opcode that we know is needed for emulating Game Boy
# Most of the info below was compiled from the very useful opcode sheet below
#  https://www.pastraiser.com/cpu/gameboy/gameboy_opcodes.html
# Trying to read through this list is rather impossible, so searching by opcode or mnemonic is your best bet.
known_instructions = [
    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None},
        executor = None),

#### TODO Check everything below here - bus_width byte_size cycles and flags may be wrong ####
    Instruction(
        0x01, "LD BC,d16", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x02, "LD (BC),A", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x03, "INC BC", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x04, "INC B", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x05, "DEC B", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x06, "LD B,d8", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x07, "RLCA", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x08, "LD (a16),SP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

### Blank ops ####
    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

### end blank ops ###

    Instruction(
        0x31, "LD SP,d16", bus_width=2,
        byte_size=2, cycles=13,
        flags={Flag.z: None, Flag.n: None, Flag.h: None, Flag.c: None}),

    Instruction(
        0x81, "ADD A,C", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: Bit.Calculate, Flag.n: Bit.Unset, Flag.h:Bit.Calculate, Flag.c: Bit.Calculate}),
]
