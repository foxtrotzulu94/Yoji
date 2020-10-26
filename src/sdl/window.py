import time

from sdl2 import *

from .constants import *

class Window:
    def __init__(self, name, width, height, scale = None, use_scale_for_window_size = False):
        self.scale = DEFAULT_SCALE if scale is None else scale
        self.width = width
        self.height = height
        if use_scale_for_window_size:
            self.width *= self.scale
            self.height *= self.scale

        SDL_Init(SDL_INIT_VIDEO)

        self.window = SDL_CreateWindow(name, 
            START_X, 
            START_Y, 
            self.width, 
            self.height, 
            SDL_WINDOW_SHOWN|SDL_WINDOW_RESIZABLE)

        self.renderer = SDL_CreateRenderer(self.window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)

        self.palette = [(0xE0, 0xDB, 0xCD, 0xFF), (0xA8, 0x9F, 0x94, 0xFF), (0x70, 0x6B, 0x66, 0xFF), (0x2B,0x2B,0x26, 0xFF)]

        self.texture = SDL_CreateTexture(self.renderer, 
            SDL_PIXELFORMAT_RGBA8888, 
            SDL_TEXTUREACCESS_TARGET, 
            self.width, 
            self.height)
        print()

        self.update_time = time.monotonic() + 1
    #end

    def Cleanup(self):
        SDL_DestroyTexture(self.texture)
        SDL_DestroyRenderer(self.renderer)
        SDL_DestroyWindow(self.window)

#end class

class VideoDebugWindow(Window):
    def __init__(self, data_func, x_tiles, num_tiles, name, scale = None):
        scale = DEFAULT_SCALE if scale is None else scale
        tile_size = GB_TILE_PIXEL_SIZE * scale
        
        self.tiles_on_x = x_tiles
        self.tiles_on_y = num_tiles // self.tiles_on_x

        width = tile_size * self.tiles_on_x + (scale * self.tiles_on_x - 1)
        height = tile_size * self.tiles_on_y + (scale * self.tiles_on_y - 1)

        super().__init__(name, width, height,  scale)
        self.read_debug_data = data_func
        
        self._hasUpdate = False
    #end

    def Tick(self):
        if not self._hasUpdate:
            return

        SDL_RenderClear(self.renderer)
        SDL_RenderCopy(self.renderer, self.texture, None, None)
        SDL_RenderPresent(self.renderer)
        self._hasUpdate = False

    def ToTiles(self,gb_2bpp):
        # Read data 16 bytes at a time to create a tile
        tile_line = []
        for i in range(0, len(gb_2bpp), 16):
            tile_line.append(gb_2bpp[i:i+16])

        # Transform each tile to pixel color
        tiles = []
        for data in tile_line:
            pixels = [ PaletteLookupTable[data[idx+1]][data[idx]] for idx in range(0, 16, 2) ]
            tiles.append( pixels )

        return tiles
    #end

    def BlitTile(self, start_x, start_y, tile):
        y = 0
        for line in tile:
            x = 0
            for pixel in line:
                color = self.palette[pixel]
                SDL_SetRenderDrawColor(self.renderer, *color)
                pixel_rect = SDL_Rect(x + start_x, y + start_y, self.scale, self.scale)
                SDL_RenderFillRect(self.renderer, pixel_rect)
                x += self.scale
            y += self.scale
        
        return (x, y)
    #end

    def Update(self):
        """TODO: OPTIMIZE"""

        if time.monotonic() < self.update_time:
            return

        gb_2bpp = self.read_debug_data()

        # Step 1: determine the actual tiles
        tiles = self.ToTiles(gb_2bpp)

        temp_ren =self.renderer
        SDL_SetRenderTarget(temp_ren, self.texture)
        SDL_SetRenderDrawColor(temp_ren, 0, 0, 0, 0xFF)

        # Step 2: actually transfer to the texture
        x_start, y_start = 0,0
        tile_count = 0
        for sprite in tiles:
            last_x, last_y = self.BlitTile(x_start, y_start, sprite)
            x_start += last_x + self.scale
            tile_count += 1

            # Go to next row by moving y_start
            if tile_count + 1 > self.tiles_on_x:
                y_start += last_y + self.scale
                x_start = 0
                tile_count = 0
        #end

        SDL_SetRenderTarget(temp_ren, None)

        self.update_time = time.monotonic() + 1
        self._hasUpdate = True