from enum import Enum, IntEnum

class IO:
    """ Input/Output register locations in memory """

    Joypad = 0xFF00
    """ Address for Input register """

    class INT(IntEnum):
        "Addresses for Interrupt Registers"
        FLAG = 0xFF0F
        ENABLE = 0xFFFF

    class LCD(IntEnum):
        "Addresses for LCD Registers"
        # General
        Ctrl = 0xFF40
        Stat = 0xFF41

        # Positioning/Scrolling
        ScrollY  = 0xFF42
        ScrollX  = 0xFF43
        LineY    = 0xFF44
        LineYCmp = 0xFF45
        WindowY  = 0xFF4A
        WindowX  = 0xFF4B

        # Palettes
        BG_data      = 0xFF47
        Sprite1_data = 0xFF48
        Sprite2_data = 0xFF49
        #TODO: CGB Palette registers

        # DMA
        DMA = 0xFF46
        # TODO: CGB DMA registers
    #end LCD

    Boot = 0xFF50
    """ Address for Boot ROM on/off """

    # TODO: Sound registers :)
#end I/O

class InterruptBit(IntEnum):
    """Bit flag for refering to System Interrupts"""

    VBlank   = 1 << 0
    LCD_STAT = 1 << 1
    Timer    = 1 << 2
    Serial   = 1 << 3
    Joypad   = 1 << 4
#end flags

class LCDCBit(IntEnum):
    """Bit flag for refering to LCD Control Register"""

    BG_Window_DisplayPriority = 1 << 0
    Sprite_DisplayEnable      = 1 << 1
    Sprite_Size               = 1 << 2
    BG_Tile_Select            = 1 << 3
    BG_Window_Data            = 1 << 4
    Window_Enable             = 1 << 5
    Window_Tile_Select        = 1 << 6
    LCD_Display_Enable        = 1 << 7
#end flags

class StatusBit(IntEnum):
    """Bit flag for refering to LCD Status"""

    Mode             = (1 | 1 << 1)
    Coincidence      = 1 << 2
    M0_HBlank_INT    = 1 << 3
    M1_VBlank_INT    = 1 << 4
    M2_OAM_INT       = 1 << 5
    Y_Coincidence_INT= 1 << 6
#end flags