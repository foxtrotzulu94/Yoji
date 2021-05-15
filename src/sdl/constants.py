from sdl2 import *

# Where to place our default window
START_X = SDL_WINDOWPOS_UNDEFINED
START_Y = SDL_WINDOWPOS_UNDEFINED

# GameBoy Viewport native Width and Height
GB_NATIVE_WIDTH = 160
GB_NATIVE_HEIGHT = 144

# GameBoy default Tile Size is 8x8
GB_TILE_PIXEL_SIZE = 8

# Upscaling factor
DEFAULT_SCALE = 2

FLAGS = SDL_WINDOW_SHOWN

# Pre-defined palettes
GB_BROWN_PALETTE = [(0xE0, 0xDB, 0xCD, 0xFF), (0xA8, 0x9F, 0x94, 0xFF), (0x70, 0x6B, 0x66, 0xFF), (0x2B,0x2B,0x26, 0xFF)]
GB_GREEN_PALETTE = [(0xE0, 0xF8, 0xD0, 0xFF), (0x88, 0xC0, 0x70, 0xFF), (0x34, 0x68, 0x56, 0xFF), (0x08,0x18,0x20, 0xFF)]
GB_GREY_PALETTE = [(0xFF, 0xFF, 0xFF, 0xFF), (0xAA, 0xAA, 0xAA, 0xFF), (0x55, 0x55, 0x55, 0xFF), (0x00,0x0,0x0, 0xFF)]

# TODO: Move somewhere?
def bit_check(val, bit):
    return ( val & (1 << bit) ) >> bit

def _get_bit_group(hi_byte, lo_byte):
    return [
        bit_check(hi_byte, bit) << 1 | bit_check(lo_byte, bit) for bit in range(7, -1, -1)
    ]

# Search as PaletteLookupTable[hi_byte][lo_byte]
PaletteLookupTable = [
    [_get_bit_group(hi_byte, lo_byte) for lo_byte in range(0, 0xFF+1)] for hi_byte in range(0, 0xFF+1)
]