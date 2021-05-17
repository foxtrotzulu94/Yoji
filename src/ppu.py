from .bus import IO, Region

from .sdl.constants import *

class PPU:
    # TODO: Caching, profiling, optimization!
    """
    Emulates the GameBoy's Pixel Processing Unit.
    Everything here is still expressed in 2 Byte per-pixel data structures
    """
    def __init__(self, memory):
        self._scroll_x = 0
        self._scroll_y = 0

        self.__test_y = 0
        # self._background
        self._memory = memory
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

    def ReadNextLine(self):
        # TODO: Actually make a nicer method and decide how this gets pushed to the LCD
        # TODO: Check the math!!!! We are reading data, but it doesn't seem to be quite right
        background = self.DebugBackgroundData()
        
        # 20 tiles make a line!
        major_idx = self.__test_y // 8
        minor_idx = self.__test_y % 8

        relevant_tiles = background[(major_idx*32) : (major_idx*32) + 20]
        line = []
        for tile in relevant_tiles:
            line += tile[minor_idx]

        self.__test_y = (self.__test_y + 1) % (GB_NATIVE_HEIGHT+1)
        return line

    def DebugTileMapData(self):
        return self.ToTileLists(self.TileData)

    def DebugBackgroundData(self):
        """Return the background map with the tile data"""
        bg = self.BackgroundMap1
        tiles = self.ToTileLists(self.TileData)
        raw_bg = [tiles[int(x)] for x in bg]
        return raw_bg

    def Tick(self):
        pass

#end class