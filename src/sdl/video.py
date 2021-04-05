import time

from sdl2 import *

import tkinter as tk
from tkinter import *

from .constants import *

class Video:
    def __init__(self, gameboy, scale = None):
        self._gb = gameboy

        # TODO: fix
        self._scale = DEFAULT_SCALE if scale is None else scale

        SDL_Init(SDL_INIT_VIDEO)
        self._width = GB_NATIVE_WIDTH * self._scale
        self._height = GB_NATIVE_HEIGHT * self._scale
        self.__tickle()

        self._window = SDL_CreateWindowFrom(self._tk_embed.winfo_id())        
        self._renderer = SDL_CreateRenderer(self._window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)

        self.__palette = [(0xE0, 0xDB, 0xCD, 0xFF), (0xA8, 0x9F, 0x94, 0xFF), (0x70, 0x6B, 0x66, 0xFF), (0x2B,0x2B,0x26, 0xFF)]
        self.__texture = SDL_CreateTexture(self._renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, self._width, self._height)

        self.__bits = [x for x in range(0,8)]
        self.__bits.reverse()
        self.__events = SDL_Event()
        self.update_time = 0

    def __exit_now(self):
        self._gb.ExitRun()

    def __tickle(self):
        def donothing():
            pass

        self._tk_root = tk.Tk()
        self._tk_root.title(b"Yoji")
        self._tk_root.resizable(False, False)

        menubar = Menu(self._tk_root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.__exit_now)
        menubar.add_cascade(label="File", menu=filemenu)

        debug_menu = Menu(menubar, tearoff=0)
        debug_menu.add_checkbutton(label="Tiles", variable = self._gb.Debug.InspectTiles, command = self._gb.Debug.ToggleInspectTiles)
        debug_menu.add_checkbutton(label="BG Map", command = self._gb.Debug.CreateWindowCommand(self._gb._ppu.DebugBackgroundData, 32, 32 * 32, b"Background data"))
        menubar.add_cascade(label="Debug", menu = debug_menu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About...", command=donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self._tk_embed = tk.Frame(self._tk_root, width = self._width, height = self._height)
        self._tk_embed.pack(side = BOTTOM)

        self._tk_root.protocol("WM_DELETE_WINDOW", self._gb.ExitRun)
        self._tk_root.config(menu=menubar)
        #self._tk_root.update()

    def Update(self):
        if time.monotonic() < self.update_time:
            return True

        self.update_time = time.monotonic() + 0.3
        try:
            # Update Tk
            self._tk_root.update()

            # Poll Events
            SDL_PollEvent(self.__events)
            if self.__events.type == SDL_QUIT or (self.__events.type == SDL_WINDOWEVENT and self.__events.window.event == SDL_WINDOWEVENT_CLOSE):
                # TODO: Close only the window that was opened instead of all of them
                self.__exit_now()
                return False

            # Clear and present whatever's in the renderer
            SDL_RenderClear(self._renderer)
            SDL_RenderCopy(self._renderer, self.__texture, None, None)
            SDL_RenderPresent(self._renderer)
            return True
        except KeyboardInterrupt:
            return False

    def Cleanup(self):
        SDL_DestroyTexture(self.__texture)
        SDL_DestroyRenderer(self._renderer)
        SDL_DestroyWindow(self._window)
        SDL_Quit()