from enum import Enum, IntEnum

class Interrupt(IntEnum):
    """Bit flag for refering to System Interrupts"""
    VBlank   = 1 << 0
    LCD_STAT = 1 << 1
    Timer    = 1 << 2
    Serial   = 1 << 3
    Joypad   = 1 << 4
#end flags