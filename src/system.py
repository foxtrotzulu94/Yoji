import logging
from sdl2 import *

from .cpu import CPU
from .ppu import PPU
from .memory import Memory
from .clock import Clock
from .cartridge import Cartridge

from .sdl.video import Video

class GameBoy:
    def __init__(self):
        self._memory = Memory(synchronized = True)
        self._cpu = CPU(self._memory)
        self._ppu = PPU(self._memory)
        self._audio = None
        self._video = Video()
        self._cart = None

        self._clock = Clock(
            self._cpu,
            self._ppu,
            self._memory,
            self._video,
            self._audio)

        self.__debug = False
        self.__log = logging.getLogger(self.__class__.__name__)
    #end

    @property
    def Debug(self):
        """ Debug mode to print instructions on each tick """
        return self.__debug

    @Debug.setter
    def Debug(self, value):
        self._cpu.Debug = self.__debug = value
        # TODO: make a debug window

    def ConfigureBIOS(self, bios_data):
        if bios_data is None:
            raise NotImplementedError()

        self._memory.SetBootRom(bios_data)
        self.__log.info("Successfully loaded BIOS")
    def SetGameRomFromFile(self, file_path):
        self._cart = Cartridge.from_file(file_path)
        self._memory.SetROM(self._cart)
        self.__log.info("Game ROM loaded: %s", file_path)

    def Run(self):
        """ Starts the GameBoy """
        self.__log.info("Starting emulation loop run")

        # TODO: Initialize systems

        events = SDL_Event()
        while True:
            try:
                # TODO: Abstract
                SDL_PollEvent(events)
                if events.type == SDL_QUIT:
                    break

                self._clock.Tick()
            except KeyboardInterrupt:
                break
        # end while
        
        self._video.Cleanup()
        self.__log.info("Shutting down")