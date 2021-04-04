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

    def __exit_now(self):
        self._gb.ExitRun()

    def __tickle(self):
        def donothing():
            pass

        self._tk_root = tk.Tk()
        self._tk_root.title(b"Yoji")

        menubar = Menu(self._tk_root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=donothing)
        filemenu.add_command(label="Open", command=donothing)
        filemenu.add_command(label="Save", command=donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.__exit_now)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=donothing)
        helpmenu.add_command(label="About...", command=donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self._tk_embed = tk.Frame(self._tk_root, width = self._width, height = self._height)
        self._tk_embed.pack(side = BOTTOM)
        def exit():
            self._gb.ExitRun()
        self._tk_root.protocol("WM_DELETE_WINDOW", exit)
        self._tk_root.config(menu=menubar)
        self._tk_root.update()

    def Tick(self):
        try:
            # Update Tk
            self._tk_root.update()

            # Poll Events
            SDL_PollEvent(self.__events)
            if self.__events.type == SDL_QUIT or (self.__events.type == SDL_WINDOWEVENT and self.__events.window.event == SDL_WINDOWEVENT_CLOSE):
                self.__exit_now()
                return False

            # Clear and present whatever's in the renderer
            SDL_RenderClear(self._renderer)
            SDL_RenderCopy(self._renderer, self.__texture, None, None)
            SDL_RenderPresent(self._renderer)
            return True
        except KeyboardInterrupt:
            return False

    def Update(self, gb_2bpp):
        """TODO: OPTIMIZE"""

        tiles = []
        for i in range(0, len(gb_2bpp), 16):
            tiles.append(gb_2bpp[i:i+16])

        # Step 1: determine the actual tiles
        rects = []
        for tile in tiles:
            blit_tile = []
            for xpos in range(0, 15, 2):
                line = []
                lsb,msb = tile[xpos], tile[xpos+1]
                for bit in self.__bits:
                    mask = 1 << bit
                    hi_bit = (msb & mask) >> bit
                    lo_bit = (lsb & mask) >> bit

                    pixel = (hi_bit << 1) | lo_bit
                    line.append( pixel )
                blit_tile.append(line)

            # tile is done
            rects.append(blit_tile)
        #end

        # Render to texture
        palette = self.__palette

        self.being_updated = True
        temp_ren =self._renderer
        SDL_SetRenderTarget(temp_ren, self.__texture)
        #SDL_RenderClear(temp_ren)
        SDL_SetRenderDrawColor(temp_ren, 0, 0, 0, 0xFF)

        # Step 2: actually transfer to the texture
        x_start,y_start = 0,0
        x_count = 0
        for blit_tile in rects:
            y = y_start
            for horizontal in blit_tile:
                x = x_start
                for pixel in horizontal:
                    color = self.__palette[pixel]
                    SDL_SetRenderDrawColor(temp_ren, *color)
                    pixel_rect = SDL_Rect(x, y, self._scale, self._scale)
                    SDL_RenderFillRect(temp_ren, pixel_rect)
                    x += self._scale
                #end
                y+= self._scale
            #end
            next_x = (x_start + (GB_TILE_PIXEL_SIZE*self._scale) + self._scale)
            x_count += 1

            # Go to next row by moving y_start
            if x_count+1 > 16 or next_x >= (self._scale * GB_NATIVE_WIDTH):
                y_start += (GB_TILE_PIXEL_SIZE * self._scale) + self._scale
                x_start = 0
                x_count = 0
            else:
                x_start = next_x
        #end

        SDL_SetRenderTarget(temp_ren, None)
        self.being_updated = False

    def Cleanup(self):
        SDL_DestroyTexture(self.__texture)
        SDL_DestroyRenderer(self._renderer)
        SDL_DestroyWindow(self._window)
        SDL_Quit()