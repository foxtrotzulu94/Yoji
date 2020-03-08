from enum import Enum, IntEnum
from .bus import IO, InterruptBit
from .catridge import Cartridge

class Memory:
    # Great resource: http://gameboy.mongenel.com/dmg/asmmemmap.html
    class Range(IntEnum):
        """Enum for refering to the Memory Ranges"""
        # ROM ranges
        ROM_BGN = 0x0000
        VECT    = 0x00FF
        BOOT_END= 0x00FF
        HEADER  = 0x014F
        ROM_0   = 0x3FFF
        ROM_XX  = 0x7FFF
        ROM_END = 0x7FFF

        # VRAM ranges
        VRAM_BGN= 0x8000
        TILE_DATA      = 0x8000
        TILE_DATA_END  = 0x97FF

        BGMAP1      = 0x9800
        BGMAP1_END  = 0x9BFF
        BGMAP2      = 0x9C00
        BGMAP2_END  = 0x9FFF
        VRAM_END= 0x9FFF

        # RAM ranges
        RAM_BGN = 0xA000
        ExtRAM  = 0xBFFF
        IntRAM  = 0xCFFF
        # GameBoy only range
        RAM_END = 0xDFFF

        # Reserved
        ECHO_RAM_BGN = 0xE000
        ECHO_RAM_END = 0xFDFF

        OAM_BGN  = 0xFE00
        OAM_END  = 0xFE9F
        UNUSABLE = 0xFEFF # Unusable

        I_O_REGS = 0xFF00
        I_O_END  = 0xFF7F

        HRAM_BGN = 0xFF80
        HRAM_END = 0xFFFE

        INT_REG = 0xFFFF
    #end flags

    def __init__(self, synchronized = False):
        # hard coding to the DMG for now
        self._boot_rom = None
        self._rom = None
        self._mem_area = bytearray(0xFFFF + 1) # Full 16-bit address space
        self._len = len(self._mem_area)
        self._ram_write_queue = None
        self._vram_write_queue = None

        self._synchronized = synchronized
        self._is_boot_active = False
    # end

    @property
    def Synchronized(self):
        """ Ensures that writes only happen after a tick """
        return self._synchronized

    @Synchronized.setter
    def Synchronized(self, value):
        self._synchronized = value
        if not value:
            # purge current write queue by
            # ticking RAM and VRAM one last time
            self.Tick()
            self.TickVRAM()
    #end

    def _is_vram_range(self, address):
        return address >= Memory.Range.VRAM_BGN and address <= Memory.Range.VRAM_END

    def _is_io_range(self, address):
        return address >= Memory.Range.I_O_REGS and address <= Memory.Range.I_O_END

    def _get_range(self, address):
        pass

    def Tick(self):
        """ Should be called for writing/refreshing Work RAM """
        if self._ram_write_queue is None:
            return

        write_args = self._ram_write_queue
        self._write_internal(*write_args)
        self._ram_write_queue = None
    def TickVRAM(self):
        """ Should be called for writing/refreshing VRAM """
        if self._vram_write_queue is None:
            return

        write_args = self._vram_write_queue
        self._write_internal(*write_args)
        self._vram_write_queue = None
    #end

    def _read_internal(self, offset, length):
        # Dispatches special memory segments
        if self._is_boot_active and offset <= Memory.Range.BOOT_END:
            return self._boot_rom[offset: offset+length]
        # if offset <= Memory.Range.ROM_END:
        #     return self._rom._data[offset: offset+length]

        # Fallback to Flat data
        return self._mem_area[offset: offset + length]
    #end

    def Read(self, offset, length = 1):
        """ Read data from Memory """
        if type(offset) is bytearray:
            offset = int.from_bytes(offset, 'little')
        return self._read_internal(offset, length)
    def readVRAMBlock(self):
        """ solely for debugging purposes """
        VRAM_SIZE = Memory.Range.VRAM_END - Memory.Range.VRAM_BGN
        return self.Read(Memory.Range.VRAM_BGN, VRAM_SIZE)
    #end

    def _write_internal(self, offset, data, length):
        # internal write method
        for i in range(0, length):
            self._mem_area[offset + i] = data[i]
    #end

    def Write(self, offset, data):
        """ Read data to memory locations """
        if type(offset) is bytearray:
            offset = int.from_bytes(offset, 'little')
        if type(data) is int:
            # We don't allow int writes larger than a byte!
            data = bytes([data])

        assert(type(data) is bytearray or type(data) is bytes)
        assert(offset > Memory.Range.ROM_END)
        size = len(data)
        if self.Synchronized:
            # queue it for a later write
            write_tuple = (offset, data, size)
            if self._is_vram_range(offset):
                assert(self._vram_write_queue is None)
                self._vram_write_queue = write_tuple
            else:
                assert(self._ram_write_queue is None)
                self._ram_write_queue = write_tuple
        else:
            # Write it directly
            self._write_internal(offset, data, size)
        #end

        # Notify anyone over a bus
        #TODO:
    #end Write

    def SetInterruptFlags(self, flags, set_bits):
        curr_val = self.CheckInterruptFlags()
        new_value = curr_val | flags if set_bits else curr_val & (~flags)
        self.Write(IO.INT.FLAG, new_value)
    def CheckInterruptFlags(self):
        return self.Read(IO.INT.FLAG)[0]
    #end

    def SetInterruptEnable(self, flags, enable):
        curr_val = self.CheckInterruptEnable()
        new_value = curr_val | flags if enable else curr_val & (~flags)
        self.Write(IO.INT.ENABLE, new_value)
    def CheckInterruptEnable(self):
        return self.Read(IO.INT.ENABLE)[0]
    #end

    def SetBootRom(self, data):
        """[Temporary]"""
        self._is_boot_active = True
        self._boot_rom = data

    def SetROM(self, rom):
        """[Temporary]"""
        self._rom = rom
        size = len(self._mem_area)
        self._mem_area = rom.GetBank() + self._mem_area[Memory.Range.VRAM_BGN:]
        new_size = len(self._mem_area)
        assert(size == new_size)