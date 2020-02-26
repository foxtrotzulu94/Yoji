class MemoryBus:
    def __init__(self):
        # hard coding to the DMG for now
        self._work_ram = bytearray(8 * 1000) # 8KB of memory
        self._video_ram = bytearray(8 * 1000) # 8KB of memory
    # end

    def ReadWorkRAM(self, offset, length):
        "WIP"
        return self._work_ram[offset: offset + length]

    def WriteWorkRAM(self, offset, data):
        "WIP"
        if type(offset) is bytearray:
            offset = int.from_bytes(offset, 'little')

        length = len(data)
        self._work_ram[offset:length] = data

    def EmplaceROMData(self, data):
        """[Temporary]"""
        self.WriteWorkRAM(0x100, data)