from sdl2 import *

from .constants import *

class Video:
    def __init__(self, scale = None):
        # TODO: fix
        self._scale = DEFAULT_SCALE if scale is None else scale

        SDL_Init(SDL_INIT_VIDEO)
        self._window = SDL_CreateWindow(b"Yoji", START_X, START_Y, GB_NATIVE_WIDTH * self._scale , GB_NATIVE_HEIGHT * self._scale , SDL_WINDOW_SHOWN|SDL_WINDOW_RESIZABLE)
        self._renderer = SDL_CreateRenderer(self._window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)

        self.__palette = [(0xE0, 0xDB, 0xCD, 0xFF), (0xA8, 0x9F, 0x94, 0xFF), (0x70, 0x6B, 0x66, 0xFF), (0x2B,0x2B,0x26, 0xFF)]
        self.__texture = SDL_CreateTexture(self._renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, GB_NATIVE_WIDTH * self._scale , GB_NATIVE_HEIGHT * self._scale)

        self.__bits = [x for x in range(0,8)]
        self.__bits.reverse()
        self.__events = SDL_Event()

    def Tick(self):
        try:
            SDL_PollEvent(self.__events)
            if self.__events.type == SDL_QUIT:
                return False

            #self.blit.wait_for(lambda: self.being_updated, None)
            # if self.being_updated:
            #     return True

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
        palette = [(0xE0, 0xDB, 0xCD, 0xFF), (0xA8, 0x9F, 0x94, 0xFF), (0x70, 0x6B, 0x66, 0xFF), (0x2B,0x2B,0x26, 0xFF)]

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