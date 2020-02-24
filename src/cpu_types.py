from enum import Enum, IntEnum

class Flag(IntEnum):
    """Enum for refering to the CPU Flags"""
    z = 7
    n = 6
    h = 5
    c = 4
#end flags

class Registers(IntEnum):
    """Enum for refering to the CPU Registers"""
    A = 0
    F = 1

    B = 2
    C = 3
    BC = 2

    D = 4
    E = 5
    DE = 4

    H = 6
    L = 7
    HL = 6

    # Special Registers
    # Do not use for indexing
    SP = -1
    PC = -2
#end

_double_registers_name={
    Registers.BC: 'BC',
    Registers.B: 'BC',
    Registers.DE: 'DE',
    Registers.D: 'DE',
    Registers.HL: 'HL',
    Registers.H: 'HL',
    Registers.SP: 'SP',
    Registers.PC: 'PC'
}

def GetRegisterName(reg, size):
    if size == 2:
        return _double_registers_name[reg]

    return reg.name
#end

class Bit(Enum):
    """Enum for determining what to do when setting a bit flag"""
    Set = 1
    Reset = 0
    Calculate = -1
    Ignore = None
#end bits