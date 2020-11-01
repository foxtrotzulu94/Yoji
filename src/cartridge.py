from enum import IntEnum
import os

class Cartridge:
    class Type(IntEnum):
        """Values for Supported ROM types"""

        ROM_ONLY = 0
        "Simplest cartridge available"

        MBC1 = 1
        "Type 1 Memory Bank Controller - Only partially supported"

        # TODO: support more types

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
    _size_id_map = {
        0x0: 32*1024, # 32KB, no switchable ROM Bank
        0x1: 64*1024 # 64KB, 4 ROM Banks
    }

    _bank_size = 16 * 1024 # 16KB

    @staticmethod
    def from_file(path):
        if not os.path.exists(path):
            return None

        data = bytearray()
        with open(path, 'rb') as cart:
            data = bytearray(cart.read())

        return Cartridge(path, data)
    #end from file

    def __init__(self, path, raw_data):
        self.name = os.path.basename(path)
        self._path = path
        self._data = raw_data
        self._rom_type = raw_data[Cartridge.Header.TYPE]
        self._rom_size_id = raw_data[Cartridge.Header.SIZE]

        self._bank = 1

        assert(Cartridge.Type.is_supported(self._rom_type))
        assert(self._rom_size_id in Cartridge._size_id_map)
        self._rom_size = Cartridge._size_id_map[self._rom_size_id]
    #end

    def ReadFixed(self, offset, length):
        return self._data[ offset : offset+length]
    def ReadMovable(self, offset, length):
        start = (self._bank * Cartridge._bank_size) + (offset - Cartridge._bank_size)
        end = start + length
        return bytearray(self._data[ start : end ])

    def ChangeBank(self, new_bank):
        if self._rom_size_id == 0x0:
            raise RuntimeError("32KB ROM requested a bank change")
        self._bank = new_bank

    def GetFixedBank(self):
        return self.GetBank(0)

    def GetCurrentBank(self):
        return self.GetBank(self._bank)

    def GetBank(self, bank):
        offset = bank * _bank_size
        return bytearray(self._data[offset: offset+_bank_size])
#end