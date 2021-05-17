from .constants import *

class LCD:
    def __init__(self, window, ppu, video_out):
        SDL_Init(SDL_INIT_VIDEO)
        self._ppu = ppu
        self._lcd_line = 0
        
        self.palette = DEFAULT_PALETTE
        self.update_time = 456
        self.next_update = 0
        # self.renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)
        # self.texture = SDL_CreateTexture(self.renderer,
        #     SDL_PIXELFORMAT_RGBA8888, 
        #     SDL_TEXTUREACCESS_TARGET, 
        #     GB_NATIVE_WIDTH, 
        #     GB_NATIVE_HEIGHT)
        self.renderer = video_out._renderer
        self.texture = video_out._texture
    # end init

    def Tick(self, cycle_num):
        if cycle_num < self.next_update:
            return

        # draw this
        data_line = self._ppu.ReadNextLine()

        SDL_SetRenderTarget(self.renderer, self.texture)
        SDL_SetRenderDrawColor(self.renderer, 0, 0, 0, 0xFF)

        x = 0
        for pixel in data_line:
            color = self.palette[pixel]
            SDL_SetRenderDrawColor(self.renderer, *color)
            pixel_rect = SDL_Rect(x, self._lcd_line, 1, 1)
            SDL_RenderFillRect(self.renderer, pixel_rect)
            x += 1

        SDL_SetRenderTarget(self.renderer, None)
        
        #FLUSH IMMEDIATE
        SDL_RenderClear(self.renderer)
        SDL_RenderCopy(self.renderer, self.texture, None, None)
        SDL_RenderPresent(self.renderer)

        self._lcd_line = (self._lcd_line + 1) % GB_NATIVE_HEIGHT
        self.next_update = cycle_num + self.update_time
    #end Tick