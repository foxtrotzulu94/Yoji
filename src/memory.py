from enum import Enum, IntEnum
from .bus import IO, Region, InterruptBit, MEMORY_RAM_CYCLES, MEMORY_VRAM_CYCLES
from .cartridge import Cartridge

class Memory:
    def __init__(self, synchronized = False):
        # hard coding to the DMG for now
        self._boot_rom = None
        self._rom = None
        self._mem_area = bytearray(0xFFFF + 1) # Full 16-bit address space
        self._len = len(self._mem_area)
        self._ram_write_queue = []

        self._synchronized = synchronized
        self._cycle_count = 0
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
            # purge current write queue
            while any(self._ram_write_queue):
                write_args = self._ram_write_queue[0][1:]
                self._write_internal(*write_args)

                del self._ram_write_queue[0]
        # end while
    #end

    @property
    def ROMName(self):
        return str(self._rom.name)

    @property
    def ROM(self):
        return self._rom

    @property
    def IsBootROMActive(self):
        """ Checks that the boot ROM is enabled or not """
        return int(self._mem_area[IO.Boot] & 0xFF) != 0
    
    @IsBootROMActive.setter
    def IsBootROMActive(self, value):
        self._mem_area[IO.Boot] = int(value)

    def _is_vram_range(self, address):
        return address >= Region.VRAM_BGN and address <= Region.VRAM_END
    def _is_tile_range(self, address):
        return address >= Region.TILE_DATA and address <= Region.TILE_DATA_END

    def _is_io_range(self, address):
        return address >= Region.I_O_REGS and address <= Region.I_O_END
    def _is_unusable_region(self, address):
        return address > Region.OAM_END and address <= Region.UNUSABLE
    def _is_ROM_region(self, address):
        return address >= Region.ROM_BGN and address <= Region.ROM_END

    def Tick(self, cycle_num):
        """ Should be called for writing/refreshing Work RAM """
        self._cycle_count = cycle_num
        # assert(len(self._ram_write_queue) < 2)
        # Check if there's anything to write
        if len(self._ram_write_queue) > 0:
            # While there's something in a queue, pop it and do it
            next_element = self._ram_write_queue[0]
            when_cycle = next_element[0]
            if cycle_num == when_cycle:
                write_args = next_element[1:]
                self._write_internal(*write_args)
                del self._ram_write_queue[0]
            else:
                # we assume the queue is ordered, 
                # so we return here immediately
                return
        # end if
    #end

    def _read_internal(self, offset, length):
        # Dispatches special memory segments

        if offset <= Region.BOOT_END and self.IsBootROMActive:
            # Read straight from the boot ROM
            return self._boot_rom[offset: offset+length]

        elif self._is_ROM_region(offset):
            # Read from the cartridge
            read_func = Cartridge.ReadFixed
            if offset > Region.ROM_0:
                read_func = Cartridge.ReadMovable

            return read_func(self._rom, offset, length)

        elif self._is_unusable_region(offset):
            # Throw an exception!
            raise RuntimeError()

        # Fallback to Flat data
        return self._mem_area[offset: offset + length]
    #end

    def Read(self, offset, length = 1):
        """ Read data from Memory """
        return self._read_internal(offset, length)
    #end

    def _write_internal(self, offset, data, length):
        # Intercept Bank switches
        if self._is_ROM_region(offset):
            self._rom.ChangeBank(int(data[0]))
            return

        # internal write method
        # TODO: Optimize!
        # It'll be easier if certain sections (like the PPU or input) are able to
        # intercept the call and handle their own memory rather than writing here
        for i in range(0, length):
            self._mem_area[offset + i] = data[i]
    #end

    def Write(self, offset, data):
        """ Read data to memory locations """
        if type(data) is int:
            # We don't allow int writes larger than a byte!
            data = bytes([data])

        size = len(data)
        if self.Synchronized:
            # queue it for a later write
            write_tuple = (offset, data, size)
            next_cycles = self._cycle_count + MEMORY_RAM_CYCLES - 1
            if self._is_vram_range(offset):
                next_cycles = self._cycle_count + MEMORY_VRAM_CYCLES - 1

            # assert(not any(self._ram_write_queue)) # or self._ram_write_queue[0][0] - next_cycles < 2)

            self._ram_write_queue.append( (next_cycles, ) + write_tuple )

        else:
            # Write it directly
            self._write_internal(offset, data, size)
        #end
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
        """Starts the Gameboy's Boot ROM"""
        self.IsBootROMActive = True
        self._boot_rom = data

    def SetROM(self, rom):
        """Sets the main Cartridge file"""
        assert(type(rom) is Cartridge)
        self._rom = rom