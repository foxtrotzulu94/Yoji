from enum import IntEnum
import os

class Cartridge:
    class Type(IntEnum):
        """Values for Supported ROM types"""

        ROM_ONLY = 0
        "Simplest cartridge available"

        # TODO: supprot more types

        @classmethod
        def is_supported(cls, value):
            return value in cls._value2member_map_
    #end

    class Header(IntEnum):
        """Addresses for Header fields"""

        START     = 0x0100
        LOGO      = 0x104
        LOGO_END  = 0x0133
        TITLE     = 0x13F
        CGB_MODE  = 0x143
        TITLE_END = 0x143
        TYPE      = 0x147
        SIZE      = 0x148
        Ext_RAM   = 0x149
        END       = 0x014F
    #end

    # TODO: support more sizes
    _sizes = {
        0x0: 32*1000 # 32KB, no ROM Bank
    }

    @staticmethod
    def from_file(path):
        if not os.path.exists(path):
            return None

        data = bytes()
        with open(path, 'rb') as cart:
            data = bytes(cart.read())

        return Cartridge(raw_data=data)
    #end from file

    def __init__(self, raw_data):
        self._data = raw_data
        self._rom_type = raw_data[Cartridge.Header.TYPE]
        self._rom_size = raw_data[Cartridge.Header.SIZE]
        assert(Cartridge.Type.is_supported(self._rom_type))
        assert(self._rom_size in Cartridge._sizes)
    #end

    def GetBank(self, bk=0):
        # TODO: keep?
        length = Cartridge._sizes[self._rom_size]
        return bytearray(self._data[0:length])
#end