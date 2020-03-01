# Great resource: http://gameboy.mongenel.com/dmg/asmmemmap.html

class Memory:
    def __init__(self):
        # hard coding to the DMG for now
        self._mem_map = bytearray(0xFFFF) # Full 16-bit address space
        self._len = len(self._mem_map)
    # end

    def Read(self, offset, length = 1):
        "WIP"
        if type(offset) is bytearray:
            offset = int.from_bytes(offset, 'little')
        return self._mem_map[offset: offset + length]

    def Write(self, offset, data):
        "WIP"
        if type(offset) is bytearray:
            offset = int.from_bytes(offset, 'little')
        if type(data) is int:
            # We don't allow longer memory!
            data = data.to_bytes(1, 'little')

        assert(type(data) is bytearray or type(data) is bytes)
        size = len(data)
        for i in range(0, size):
            self._mem_map[offset + i] = data[i]
        assert(self._len == len(self._mem_map))

    def LoadROM(self, data):
        """[Temporary]"""
        self.Write(0x100, data)