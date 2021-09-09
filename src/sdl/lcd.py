from .constants import *

class LCD:
    def __init__(self, video_out):
        SDL_Init(SDL_INIT_VIDEO)
        self._lcd_line = 0
        
        self.palette = DEFAULT_PALETTE
        self.update_time = 30
        self.next_update = 0
        self.renderer = video_out._renderer
        self.texture = video_out._texture
        self.data_line = None
    # end init

    def PixelLineCallback(self, data_line):
        self.data_line = data_line
        # no need to protect this variable since it is all single threaded

    def Tick(self, cycle_num):
        if self.data_line is None:
            return

        # draw this
        data_line = self.data_line

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

        self._lcd_line = (self._lcd_line + 1) % (GB_NATIVE_HEIGHT + 1)
        self.next_update = cycle_num + self.update_time
        self.data_line = None
    #end Tick