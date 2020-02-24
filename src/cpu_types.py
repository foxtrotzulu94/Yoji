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
    D = 4
    E = 5
    H = 6
    L = 7
#end

class Bit(Enum):
    """Enum for determining what to do when setting a bit flag"""
    Set = 1
    Reset = 0
    Calculate = -1
    Ignore = None
#end bits