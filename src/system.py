import logging
from sdl2 import *
from .sdl.window import VideoDebugWindow

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

    def _handle_events(self):
        pass

    def Run(self):
        """ Starts the GameBoy """
        self.__log.info("Starting emulation loop run")        

        # TODO: Initialize systems
        tile_debug = VideoDebugWindow(self._ppu.DebugTileMapData, 16, 384, b"Tile data")
        bg_debug = VideoDebugWindow(self._ppu.DebugBackgroundData, 32, 32 * 32, b"Background data")

        events = SDL_Event()
        while True:
            try:
                # TODO: Abstract
                SDL_PollEvent(events)
                if events.type == SDL_QUIT:
                    break
                elif events.type == SDL_WINDOWEVENT and events.window.event == SDL_WINDOWEVENT_CLOSE:
                    break

                self._clock.Tick()
                tile_debug.Update()
                tile_debug.Tick()

                bg_debug.Update()
                bg_debug.Tick()
            except KeyboardInterrupt:
                break
        # end while
        
        self._video.Cleanup()
        tile_debug.Cleanup()
        self.__log.info("Shutting down")