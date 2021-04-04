import logging
from sdl2 import *
from .sdl.window import VideoDebugWindow

from .cpu import CPU
from .ppu import PPU
from .memory import Memory
from .clock import Clock
from .cartridge import Cartridge
from .bus import *

from .debug import Debug

from .sdl.video import Video

class GameBoy:
    def __init__(self):
        self._memory = Memory(synchronized = True)
        self._cpu = CPU(self._memory)
        self._ppu = PPU(self._memory)
        self._audio = None
        self._cart = None
        self._clock = Clock(
            self._cpu,
            self._ppu,
            self._memory,
            None, #self._screen,
            self._audio)

        # TODO: Merge logging and debugging
        self.__debug = Debug(self._cpu, self._memory)
        self.__log = logging.getLogger(self.__class__.__name__)

        self._screen = Video(self)

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
            self._initializeSystemNoBIOS()
            self.__log.info("Successfully Bootstrapped DMG mode")
            return

        self._memory.SetBootRom(bios_data)
        self.__log.info("Successfully loaded BIOS")

    def SetGameRomFromFile(self, file_path):
        self._cart = Cartridge.from_file(file_path)
        self._memory.SetROM(self._cart)
        self.__log.info("Game ROM loaded: %s", file_path)

    def _debug_tick(self, debug_objs):
        for thing in debug_objs:
            thing.Tick()

    def _initializeSystemNoBIOS(self):
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
            self._initializeSystemNoBIOS()

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