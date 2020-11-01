from .cpu import CPU
from .ppu import PPU
from .memory import Memory
from .clock import Clock
from .cartridge import Cartridge
from .bus import *

class Debug:
    def __init__(self, cpu : CPU, mem: Memory):
        self._cpu = cpu
        self._memory = mem
    
    def disassemble_rom(self, filename = None):
        # get some basic info about the ROM
        rom_type = self._memory._rom._rom_type
        rom_size = self._memory._rom._rom_size
        bank_size = Cartridge._bank_size
        banks = rom_size // bank_size

        self._memory.IsBootROMActive = False

        if filename is None:
            filename = self._memory.ROMName + ".dump"

        with open(filename, 'w') as dump_file:
            dump_file.write("; Decompilation of ")
            dump_file.write(self._memory.ROMName)
            dump_file.write("\nAddress   Opcode   Mnemonic\n")

            # Scan the whole thing, start at 0
            self._cpu.PC = 0x0
            while self._cpu.PC <= Region.ROM_0:
                self._cpu.Dump(True, dump_file)

            # switch and scan all the banks successively
            for i in range(1, banks):
                self._memory.ROM.ChangeBank(i)
                self._cpu.PC = Region.ROM_0+1    
                
                while self._cpu.PC <= Region.ROM_XX:
                    self._cpu.Dump(True, dump_file)

