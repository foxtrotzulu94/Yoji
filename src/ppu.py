from enum import IntEnum, auto
import time

from .bus import IO, Region

from .sdl.constants import *

class PPU:
    # TODO: Caching, profiling, optimization!
    """
    Emulates the GameBoy's Pixel Processing Unit.
    Everything here is still expressed in 2 Byte per-pixel data structures
    """
    class State(IntEnum):
        MODE_0 = 1
        MODE_1 = 1
        OAM_SEARCH = 5
        H_BLANK = 3
        V_BLANK = 4

    def __init__(self, memory, lcd):
        self._lcd = lcd
        self._scroll_x = 0
        self._scroll_y = 0

        self.__test_y = 0
        # self._background
        self._memory = memory
        self._next_instr_cycle =0
        self._state = PPU.State.MODE_0
        self._cache_pixels = None
        self.checkpoint = None
    #end

    @property
    def BackgroundMap1(self):
        return self._memory.Read(Region.BGMAP1, Region.BGMAP1_END+1 - Region.BGMAP1)

    @property
    def TileData(self):
        tile_data_size = Region.TILE_DATA_END - Region.TILE_DATA + 1
        return self._memory.Read(Region.TILE_DATA, tile_data_size)

    def ToTileLists(self, gb_2bpp):
        # Read data 16 bytes at a time to create a tile
        # tile_line = []
        # for i in range(0, len(gb_2bpp), 16):
        #     tile_line.append()

        # Transform each tile to pixel color
        tiles = []
        #for data in tile_line:
        for i in range(0, len(gb_2bpp), 16):
            data = gb_2bpp[i:i+16]
            pixels = [ PaletteLookupTable[data[idx+1]][data[idx]] for idx in range(0, 16, 2) ]
            tiles.append( pixels )

        return tiles
    #end

    def ReadNextLine(self):
        # TODO: Actually make a nicer method and decide how this gets pushed to the LCD
        background = self.DebugBackgroundData()

        # NOTE:
        # 'background' is a flat list of tiles, which themselves are 8x8 entries of 1's and 0's
        # (e.g. background[0] -> list[8][8]), this is the PPU internal representation that is easy to scale and transform
        # The background map is made up of 32x32 tiles, hence each line has 32
        # Given that, we need two indices: major_idx to select the tiles that will be rendered (this slice becomes relevant_tiles)
        #                                  minor_idx to determine which pixels of said tiles need to be sent over
        # This operation would be simpler if 'background' were a true 2D bitmap
        # NOTE that one thing that is not handled is any x offset (as would be needed for true viewport functionality)
        # NOTE we also do not handle writing any LCD status registers backs

        # floor with int divide by 8, multiply by the amount to skip once we finish a line
        major_idx = (self.__test_y // 8) * 32 # TODO: we'd add an x-offset somewhere in this line
        minor_idx = self.__test_y % 8

        # 20 tiles make a display line!
        relevant_tiles = background[major_idx : major_idx + 20]
        line = []
        for tile in relevant_tiles:
            line += tile[minor_idx]

        self.__test_y = (self.__test_y + 1) #% (GB_NATIVE_HEIGHT+1)
        return line

    def DebugTileMapData(self):
        return self.ToTileLists(self.TileData)

    def DebugBackgroundData(self):
        """Return the background map with the tile data"""
        bg = self.BackgroundMap1
        tiles = self.ToTileLists(self.TileData)
        raw_bg = [tiles[int(x)] for x in bg]
        return raw_bg

    def Tick(self, cycle_num):
        if cycle_num < self._next_instr_cycle:
            return

        # what mode were we in?
        proc_cycles = 0
        if self._state == PPU.State.V_BLANK:
            self.checkpoint = time.monotonic()
            self._state = PPU.State.OAM_SEARCH
        if self._state == PPU.State.OAM_SEARCH:
            proc_cycles = 20
            self._state = PPU.State.MODE_0
            # TODO: set interrupts, do some partial processing

        elif self._state == PPU.State.MODE_0:
            self._lcd.PixelLineCallback(self.ReadNextLine())
            proc_cycles = 43
            self._state = PPU.State.H_BLANK

        elif self._state == PPU.State.H_BLANK:
            proc_cycles = 51
            self._state = PPU.State.OAM_SEARCH
            # TODO: set interrupts, do some partial processing

        if self.__test_y == (GB_NATIVE_HEIGHT+1):
            # v-blank time
            # TODO: verify behaviour
            self._state = PPU.State.V_BLANK
            proc_cycles = (20+43+51) * 10
            self.__test_y = 0
            if self.checkpoint is not None:
                duration = time.monotonic() - self.checkpoint
                #print(f"Full screen render took {duration} seconds")
                #print("complete")

        self._next_instr_cycle = cycle_num+proc_cycles

#end class