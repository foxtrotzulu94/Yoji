# Great resource: http://gameboy.mongenel.com/dmg/asmmemmap.html

class MemoryBus:
    def __init__(self):
        # hard coding to the DMG for now
        self._mem_map = bytearray(0xFFFF) # Full 16-bit address space
    # end

    def ReadWorkRAM(self, offset, length):
        "WIP"
        return self._mem_map[offset: offset + length]

    def WriteWorkRAM(self, offset, data):
        "WIP"
        if type(offset) is bytearray:
            offset = int.from_bytes(offset, 'little')

        length = len(data)
        self._mem_map[offset:length] = data

    def EmplaceROMData(self, data):
        """[Temporary]"""
        self.WriteWorkRAM(0x100, data)