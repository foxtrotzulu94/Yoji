from sdl2 import *
from threading import Thread
import threading

X = Y = SDL_WINDOWPOS_UNDEFINED
SIZE = 4
GB_NATIVE_WIDTH = 160
GB_NATIVE_HEIGHT = 144

class Window:
    def __init__(self):
        SDL_Init(SDL_INIT_VIDEO)
        self.win = SDL_CreateWindow(b"VRAM", X, Y, GB_NATIVE_WIDTH*4, GB_NATIVE_HEIGHT*4, SDL_WINDOW_SHOWN|SDL_WINDOW_RESIZABLE)
        self.ren = SDL_CreateRenderer(self.win, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)
        self.being_updated = False
        self.tex = SDL_CreateTexture(self.ren, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, 4*GB_NATIVE_WIDTH, 4*GB_NATIVE_WIDTH)
        self.blit = threading.Condition()

    def Update(self, gb_2bpp):
        tiles = []
        for i in range(0, len(gb_2bpp), 16):
            tiles.append(gb_2bpp[i:i+16])

        rects = []
        bits = [x for x in range(0,8)]
        bits.reverse()

        for tile in tiles:
            blit_tile = []
            for xpos in range(0, 16, 2):
                line = []
                lsb,msb = tile[xpos], tile[xpos+1]
                for bit in bits:
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
        temp_ren =self.ren# SDL_CreateRenderer(self.win, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)
        SDL_SetRenderTarget(temp_ren, self.tex)
        SDL_RenderClear(temp_ren)
        SDL_SetRenderDrawColor(temp_ren, 0, 0, 0, 0xFF)

        x_start,y_start = 0,0
        for blit_tile in rects:
            y = y_start
            for horizontal in blit_tile:
                x = x_start
                for pixel in horizontal:
                    color = palette[pixel]
                    SDL_SetRenderDrawColor(temp_ren, *color)
                    pixel_rect = SDL_Rect(x, y, SIZE, SIZE)
                    SDL_RenderFillRect(temp_ren, pixel_rect)
                    x += SIZE
                #end
                y+= SIZE
            #end
            x_start = (x_start + (8*SIZE) + 4)
            if (x_start + (8*SIZE)) > 4*GB_NATIVE_WIDTH:
                y_start += (8*SIZE) + 4
                x_start = 0
        #end

        SDL_SetRenderTarget(temp_ren, None)
        # SDL_DestroyRenderer(temp_ren)
        self.being_updated = False

    def Run(self):
        # SDL_Init(SDL_INIT_VIDEO)
        render = True
        thing = SDL_Event()

        # SDL_SetRenderDrawColor(self.ren, 0xFF, 0xFF, 0xFF, 0xFF)
        while(render):
            try:
                SDL_PollEvent(thing)
                if thing.type == SDL_QUIT:
                    render = False
                    continue

                #self.blit.wait_for(lambda: self.being_updated, None)
                if self.being_updated:
                    continue

                SDL_RenderClear(self.ren)
                SDL_RenderCopy(self.ren, self.tex, None, None)
                SDL_RenderPresent(self.ren)
            except KeyboardInterrupt:
                render = False

        SDL_DestroyTexture(self.tex)
        SDL_DestroyRenderer(self.ren)
        SDL_DestroyWindow(self.win)
        SDL_Quit()
    #

    def RunThread(self):
        t = Thread(target=Window.Run, args=(self,))
        t.start()
        return t

def render_tile(gb_2bpp):
    tiles = []
    for i in range(0, len(gb_2bpp), 16):
        tiles.append(gb_2bpp[i:i+16])

    rects = []
    bits = [x for x in range(0,8)]
    bits.reverse()

    for tile in tiles:
        blit_tile = []
        for xpos in range(0, 16, 2):
            line = []
            lsb,msb = tile[xpos], tile[xpos+1]
            for bit in bits:
                mask = 1 << bit
                hi_bit = (msb & mask) >> bit
                lo_bit = (lsb & mask) >> bit

                pixel = (hi_bit << 1) | lo_bit
                line.append( pixel )
            blit_tile.append(line)
        # tile is done
        rects.append(blit_tile)
    #end

    SDL_Init(SDL_INIT_VIDEO)
    X = Y = SDL_WINDOWPOS_UNDEFINED
    SIZE = 4
    GB_NATIVE_WIDTH = 160
    GB_NATIVE_HEIGHT = 144
    win = SDL_CreateWindow(b"VRAM", X, Y, GB_NATIVE_WIDTH * SIZE, GB_NATIVE_HEIGHT * SIZE, SDL_WINDOW_SHOWN|SDL_WINDOW_RESIZABLE)
    ren = SDL_CreateRenderer(win, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)

    # Render to texture
    palette = [(0xE0, 0xDB, 0xCD, 0xFF), (0xA8, 0x9F, 0x94, 0xFF), (0x70, 0x6B, 0x66, 0xFF), (0x2B,0x2B,0x26, 0xFF)]
    tex = SDL_CreateTexture(ren, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, GB_NATIVE_WIDTH * SIZE, GB_NATIVE_HEIGHT * SIZE)
    SDL_SetRenderTarget(ren, tex)

    SDL_RenderClear(ren)
    SDL_SetRenderDrawColor(ren, 0, 0, 0, 0xFF)

    x_start,y_start = 0,0
    for blit_tile in rects:
        y = y_start
        for horizontal in blit_tile:
            x = x_start
            for pixel in horizontal:
                color = palette[pixel]
                SDL_SetRenderDrawColor(ren, *color)
                pixel_rect = SDL_Rect(x, y, SIZE, SIZE)
                SDL_RenderFillRect(ren, pixel_rect)
                x += SIZE
            #end
            y+= SIZE
        #end
        x_start = (x_start + (8*SIZE) + 4)
        if (x_start + (8*SIZE)) > 4*GB_NATIVE_WIDTH:
            y_start += (8*SIZE) + 4
            x_start = 0
    #end

    SDL_SetRenderTarget(ren, None)

    render = True
    thing = SDL_Event()
    Drawing = SDL_Rect(0,0,8*SIZE,8*SIZE)

    SDL_SetRenderDrawColor(ren, 0xFF, 0xFF, 0xFF, 0xFF)
    while(render):
        try:
            SDL_PollEvent(thing)
            if thing.type == SDL_QUIT:
                render = False
                continue
            SDL_RenderClear(ren)
            SDL_RenderCopy(ren, tex, None, None)
            SDL_RenderPresent(ren)
        except KeyboardInterrupt:
            render = False

    SDL_DestroyTexture(tex)
    SDL_DestroyRenderer(ren)
    SDL_DestroyWindow(win)
    SDL_Quit()
#end

def test_window():
    gb_2bpp = bytearray(int(x, base=16) for x in "FF 00 7E FF 85 81 89 83 93 85 A5 8B C9 97 7E FF".split())
    render_tile(gb_2bpp)
#end

def main():
    # test_window()
    testy = Window()
    gb_2bpp = bytearray(int(x, base=16) for x in "FF 00 7E FF 85 81 89 83 93 85 A5 8B C9 97 7E FF".split())
    testy.Update(gb_2bpp)
    testy.Run()

if __name__ == "__main__":
    main()