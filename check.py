from src.cpu import CPU
from src.memory import Memory
from src.instructions import *

from sdl2 import *

def render_tiles(gb_2bpp):
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
    win = SDL_CreateWindow(b"VRAM", X, Y, GB_NATIVE_WIDTH*4, GB_NATIVE_HEIGHT*4, SDL_WINDOW_SHOWN)
    ren = SDL_CreateRenderer(win, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)

    # Render to texture
    palette = [(0xE0, 0xDB, 0xCD, 0xFF), (0xA8, 0x9F, 0x94, 0xFF), (0x70, 0x6B, 0x66, 0xFF), (0x2B,0x2B,0x26, 0xFF)]
    tex = SDL_CreateTexture(ren, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, 4*GB_NATIVE_WIDTH, 4*GB_NATIVE_WIDTH)
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

def test_instructions():
    mem = Memory()
    cpu = CPU(mem)

    cpu.H = 0xED
    cpu.executeArbitraryInstruction("SWAP H")
    assert(cpu.H == 0xDE)

    cpu.executeArbitraryInstruction("CCF")
    assert(cpu.c)
    cpu.executeArbitraryInstruction("CCF")
    assert(not cpu.c)
    cpu.executeArbitraryInstruction("SCF")
    assert(cpu.c)

    val = cpu.SP = 0xfffe
    cpu.BC = 0xbeef
    assert(cpu.BC == 0xbeef)
    print(mem.Read(cpu.SP, 1))
    cpu.executeArbitraryInstruction("PUSH BC")

    cpu.BC = 0xc0fe
    print(mem.Read(cpu.SP, 2))
    cpu.executeArbitraryInstruction("PUSH BC")

    print(mem.Read(cpu.SP, 4))
    cpu.executeArbitraryInstruction("LD BC,d16")
    assert(cpu.BC == 0x0)

    cpu.executeArbitraryInstruction("POP BC")
    print(mem.Read(cpu.SP, 2))
    cpu.executeArbitraryInstruction("POP BC")
    print(mem.Read(cpu.SP, 1))

    assert(cpu.BC == 0xbeef)
#end

def test_window():
    data = "CE ED 66 66 CC 0D 00 0B 03 73 00 83 00 0C 00 0D 00 08 11 1F 88 89 00 0E DC CC 6E E6 DD DD D9 99 BB BB 67 63 6E 0E EC CC DD DC 99 9F BB B9 33 3E"
    data ="FF 00 7E FF 85 81 89 83 93 85 A5 8B C9 97 7E FF"
    gb_2bpp = bytearray(int(x, base=16) for x in data.split())
    render_tiles(gb_2bpp)
#end

def main():
    test_window()
#end

if __name__ == "__main__":
    main()