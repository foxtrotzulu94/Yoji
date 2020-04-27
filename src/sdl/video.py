from sdl2 import *

START_X = SDL_WINDOWPOS_UNDEFINED
START_Y = SDL_WINDOWPOS_UNDEFINED
GB_NATIVE_WIDTH = 160
GB_NATIVE_HEIGHT = 144
DEFAULT_SCALE = 3
FLAGS = SDL_WINDOW_SHOWN

class Video:
    def __init__(self, scale = None):
        self._scale = DEFAULT_SCALE if scale is None else scale
        pass