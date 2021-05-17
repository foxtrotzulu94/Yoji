import logging
import sys

from sdl2 import *
from .sdl.window import VideoDebugWindow

from .cpu import CPU
from .ppu import PPU
from .memory import Memory
from .clock import Clock
from .cartridge import Cartridge
from .bus import *

from .sdl.video import Video
from .sdl.lcd import LCD

class GameBoy:
    def __init__(self):
        # TODO: Merge logging and debugging
        self.__debug = Debug(self)
        self.__log = logging.getLogger(self.__class__.__name__)
        self._screen = Video(self)

        self._memory = Memory(synchronized = True)
        self._cpu = CPU(self._memory)
        self._ppu = PPU(self._memory)
        self._lcd = LCD(self._screen._window, self._ppu, self._screen)
        self._audio = None
        self._cart = None
        self._clock = Clock(
            self._cpu,
            self._ppu,
            self._memory,
            self._lcd,
            self._audio)

        self._init_complete = False
        self._ticking = False
    #end

    @property
    def Debug(self):
        """ Property to access the Debug window """
        return self.__debug

    def ExitRun(self):
        """ Indicates that ticking should stop, halting any existing runs """
        self._ticking = False        

    def ConfigureBIOS(self, bios_data):
        if bios_data is None:
            self._initialize_without_bios()
            self.__log.info("Successfully Bootstrapped DMG mode")
            return

        self._memory.SetBootRom(bios_data)
        self.__log.info("Successfully loaded BIOS")

    def SetGameRomFromFile(self, file_path):
        self._cart = Cartridge.FromFile(file_path)
        self._memory.SetROM(self._cart)
        self.__log.info("Game ROM loaded: %s", file_path)

    def _debug_tick(self, debug_objs):
        for thing in debug_objs:
            thing.Tick()

    def _initialize_without_bios(self):
        """ Sets the system to the initial state of a DMG (Original GameBoy) """
        if self._init_complete:
            return
        
        self._cpu.AF = 0x01B0
        self._cpu.BC = 0x0013
        self._cpu.DE = 0x00D8
        self._cpu.HL = 0x014D
        self._cpu.SP = 0xFFFE
        self._cpu.PC = 0x100

        self._memory.Synchronized = False
        # Init Timers
        self._memory.Write(IO.Timer.TIMA, 00)
        self._memory.Write(IO.Timer.TMA, 00)
        self._memory.Write(IO.Timer.TAC, 00)
        # Init Sound (Noise Registers)
        # TODO: IO.Sound.NR*
        # Init LCD
        self._memory.Write(IO.LCD.LCDC, 0x91)
        self._memory.Write(IO.LCD.SCX, 00)
        self._memory.Write(IO.LCD.SCY, 00)
        self._memory.Write(IO.LCD.LYC, 00)
        self._memory.Write(IO.LCD.BGP, 0xFC)
        self._memory.Write(IO.LCD.OBP0, 0xFF)
        self._memory.Write(IO.LCD.OBP1, 0xFF)
        self._memory.Write(IO.LCD.WX, 00)
        self._memory.Write(IO.LCD.WY, 00)
        self._memory.Synchronized = True
        
        # Don't re-run
        self._init_complete = True
        

    def Run(self):
        """ Starts the GameBoy """
        self.__log.info("Starting emulation loop run")

        # If a boot ROM wasn't set, auto initialize
        if not self._memory.IsBootROMActive and not self._init_complete:
            self._initialize_without_bios()

        self._ticking = True
        while self._ticking:
            try:
                keep_running = self._screen.Update()
                if not keep_running:
                    break

                self._clock.Update()
                self.__debug.Update()
            except KeyboardInterrupt:
                break
        # end while
        self._ticking = False
        
        self._screen.Cleanup()
        self.__debug.Cleanup()
        self.__log.info("Shutting down")
    #end run
#end GameBoy

class Debug:

    def __init__(self, gameboy: GameBoy):
        from collections import OrderedDict

        self._gb = gameboy
        self._active = False

        self._breakpoints = []
        self._bgmap_inspect_window = None
        self._tile_inspect_window = None
        self._inspect_windows = []

    def __generate_inspect_window_property(key, documentation, data_func, x_tiles, num_tiles):
        def get(self):
            return self.has_key(key)
        def set(self, value):
            if value:
                window = VideoDebugWindow(data_func, x_tiles, num_tiles, key)
                self._inspect_windows[key] = window
            else:
                window = self._inspect_windows[key]
                window.Cleanup()
                del self._inspect_windows[key]
        return property(get, set, None, documentation)
    #end

    @property
    def Active(self):
        return self._active
    @Active.setter
    def Active(self, value):
        self._active = value

    @property
    def InspectTiles(self):
        return self._tile_inspect_window != None
    @InspectTiles.setter
    def InspectTiles(self, value):
        if value:
            self._tile_inspect_window = VideoDebugWindow(self._gb._ppu.DebugTileMapData, 16, 384, b"Tile data")
            self._inspect_windows.append(self._tile_inspect_window)
        else:
            self._inspect_windows.remove(self._tile_inspect_window)
            self._tile_inspect_window.Cleanup()
            self._tile_inspect_window = None
    #end

    @property
    def InspectBackgroundMap(self):
        return self._bgmap_inspect_window != None
    @InspectBackgroundMap.setter
    def InspectBackgroundMap(self, value):
        if value:
            self._bgmap_inspect_window = VideoDebugWindow(self._gb._ppu.DebugBackgroundData, 32, 32 * 32, b"Background data")
            self._inspect_windows.append(self._bgmap_inspect_window)
        else:
            self._inspect_windows.remove(self._bgmap_inspect_window)
            self._bgmap_inspect_window.Cleanup()
            self._bgmap_inspect_window = None
    #end

    def ToggleInspectTiles(self):
        self.InspectTiles = not self.InspectTiles
    def ToggleInspectBackgroundMap(self):
        self.InspectBackgroundMap = not self.InspectBackgroundMap

    def Update(self):
        for window in self._inspect_windows:
            window.Update()
    #end

    def Cleanup(self):
        for window in self._inspect_windows:
            window.Cleanup()

    def execute_cpu_instruction(self, opcode):
        """ Runs an arbitrary instruction once """
        
        cpu = self._gb._cpu
        instr = None
        # Instruction decode
        if type(opcode) is int:
            instr = cpu.__base_opcodes[opcode]
            if (opcode & 0xFF00) == 0xCB00:
                opcode = (opcode >> 8)
                instr = self.__cb_opcodes[opcode]
        elif type(opcode) is str:
            # This is pretty darn slow...
            matching = [ x for x in __base_opcodes + __cb_opcodes if x._mnemonic == opcode ]
            if len(matching) < 1:
                raise KeyError("Mnemonic not found!")
            instr = matching[0]
        #end

        # Instruction Execute
        location = cpu.PC + 1
        print(instr.ToString(self.__memory, self.PC))
        result = instr.execute(self, self.__memory, location)

        # Writeback
        instr.writeback(self, self.__memory, location, result)
        self._check_interrupts()
    #end

    def print_cpu_instruction(self, output_handle = sys.stdout):
        # Fetch, Decode and dump
        cpu = self._gb._cpu
        cpu._get_next_instruction()
        output_handle.write(cpu._curr_inst.ToString(self._gb._memory, cpu.PC))
        output_handle.write('\n')
    
    def dump_rom(self, filename = None):
        # get some basic info about the ROM
        mem_bus = self._gb._memory
        rom_type = mem_bus._rom._rom_type
        rom_size = mem_bus._rom._rom_size
        bank_size = Cartridge._bank_size
        banks = rom_size // bank_size

        mem_bus.IsBootROMActive = False

        if filename is None:
            filename = mem_bus.ROMName + ".dump"

        with open(filename, 'w') as dump_file:
            dump_file.write("; Decompilation of ")
            dump_file.write(mem_bus.ROMName)
            dump_file.write("\nAddress   Opcode   Mnemonic\n")

            # Scan the whole thing, start at 0
            cpu = self._gb._cpu
            cpu.PC = 0x0
            while cpu.PC <= Region.ROM_0:
                self.print_cpu_instruction(dump_file)
                cpu.PC += max(cpu._curr_inst.Size, 1)

            # switch and scan all the banks successively
            for i in range(1, banks):
                mem_bus.ROM.ChangeBank(i)
                cpu.PC = Region.ROM_0+1    
                
                while cpu.PC <= Region.ROM_XX:
                    self.print_cpu_instruction(dump_file)
                    cpu.PC += max(cpu._curr_inst.Size, 1)
    #end dump
#end debugger