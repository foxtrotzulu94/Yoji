import time

from sdl2 import *

from .constants import *

class Window:
    def __init__(self, name, width, height, scale = DEFAULT_SCALE):
        self.width = width
        self.height = height
        self.scale = scale
        self.palette = GB_GREY_PALETTE

        SDL_Init(SDL_INIT_VIDEO)
        self.window = SDL_CreateWindow(name, 
            START_X, 
            START_Y, 
            # SDL will stretch the texture to the size of the window
            self.width * self.scale, 
            self.height * self.scale, 
            SDL_WINDOW_SHOWN|SDL_WINDOW_RESIZABLE)

        self.renderer = SDL_CreateRenderer(self.window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)
        self.texture = SDL_CreateTexture(self.renderer, 
            SDL_PIXELFORMAT_RGBA8888, 
            SDL_TEXTUREACCESS_TARGET, 
            self.width, 
            self.height)

        self.update_time = time.monotonic() + 1
    #end

    def Cleanup(self):
        SDL_DestroyTexture(self.texture)
        SDL_DestroyRenderer(self.renderer)
        SDL_DestroyWindow(self.window)
#end class

class VideoDebugWindow(Window):
    def __init__(self, data_func, x_tiles, num_tiles, name, scale = DEFAULT_SCALE):        
        self.tiles_on_x = x_tiles
        self.tiles_on_y = num_tiles // self.tiles_on_x
        self.tile_border = 1

        # Size of the tile 8x8 and its border
        width = (GB_TILE_PIXEL_SIZE * self.tiles_on_x) + (self.tile_border * self.tiles_on_x - 1)
        height = (GB_TILE_PIXEL_SIZE * self.tiles_on_y) + (self.tile_border * self.tiles_on_y - 1)

        super().__init__(name, width, height,  scale)
        self.__read_debug_data = data_func
    #end

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
        # Blit each pixel in native res, one at a time
        # There are probably more efficient ways of doing this with SIMD and/or caching structures
        # We do it naively here to be able to debug more easily.

        y = 0
        for line in tile:
            x = 0
            for pixel in line:
                color = self.palette[pixel]
                SDL_SetRenderDrawColor(self.renderer, *color)
                pixel_rect = SDL_Rect(x + start_x, y + start_y, 1, 1)
                SDL_RenderFillRect(self.renderer, pixel_rect)
                x += 1
            y += 1
        
        return (x, y)
    #end

    def __draw_to_texture(self, tiles):
        SDL_SetRenderTarget(self.renderer, self.texture)
        SDL_SetRenderDrawColor(self.renderer, 0, 0, 0, 0xFF)

        x_start, y_start = 0,0
        tile_count = 0
        for sprite in tiles:
            last_x, last_y = self.BlitTile(x_start, y_start, sprite)
            x_start += last_x + self.tile_border
            tile_count += 1

            # Go to next row by moving y_start
            if tile_count + 1 > self.tiles_on_x:
                y_start += last_y + self.tile_border
                x_start = 0
                tile_count = 0
        #end

        SDL_SetRenderTarget(self.renderer, None)
    #end draw

    def __present_texture(self):
        SDL_RenderClear(self.renderer)
        SDL_RenderCopy(self.renderer, self.texture, None, None)
        SDL_RenderPresent(self.renderer)
    # end present

    def Update(self):
        if time.monotonic() < self.update_time:
            return

        # Update has 3 steps:
        # 1) Read the relevant data
        # 2) Draw it to a texture
        # 3) Present the texture by copying it to the screen
        tiles = self.__read_debug_data()
        self.__draw_to_texture(tiles)
        self.__present_texture()

        self.update_time = time.monotonic() + 5
    #end Update
#end VideoDebugWindow