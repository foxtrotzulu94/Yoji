from .cpu_types import *
from .instructions import *

# The list below is every single opcode that we know is needed for emulating Game Boy
# Most of the info below was compiled from the very useful opcode sheet below
#  https://www.pastraiser.com/cpu/gameboy/gameboy_opcodes.html
# Trying to read through this list is rather impossible, so searching by opcode or mnemonic is your best bet.
known_instructions = [
    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = None, executor = None),

    Instruction(
        0x01, "LD BC,d16", bus_width=2,
        byte_size=3, cycles=12,
        flags=None,
        operands = ( Operand.reg(Registers.BC, 2), Operand.imm(2) ),
        executor = Load),

    Instruction(
        0x02, "LD (BC),A", bus_width=1,
        byte_size=1, cycles=4,
        flags=None),

#### TODO Check everything below here - bus_width byte_size cycles and flags may be wrong ####
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
        flags=None,
        operands = ( Operand.reg(Registers.SP, 2), Operand.imm(2) ),
        executor = Load),

    Instruction(
        0x81, "ADD A,C", bus_width=1,
        byte_size=1, cycles=4,
        flags={Flag.z: Bit.Calculate, Flag.n: Bit.Reset, Flag.h:Bit.Calculate, Flag.c: Bit.Calculate}),
]