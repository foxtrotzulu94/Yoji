import time

class Clock:
    """
    Emulates the System master clock by subdividing the machine cycle @ 4MHz
    """

    def __init__(self, cpu, ppu, memory, video_out, audio):
        self._cpu = cpu
        self._ppu = ppu
        self._memory = memory
        self._lcd = video_out
        self._audio = audio

        self._cycles = 0
        self._time = 0
        self._should_run = True
        self._is_ticking = False
    #end

    def _tick_timers(self):
        # TODO: tick any hardware timers
        pass

    def Tick(self):
        # We divide out main loop among the components
        # Keep in mind the timings and the order

        # TODO: Rather than subdiving, pass the machine cycles as an argument for synchronization
        # This came after an assertion error in the Memory Write Queue. Presumably we flushed an earlier write
        # but there were back to back write instructions
        # Specifically from Blarg's CPU test
        # Address   Opcode   Mnemonic
        # 0x02DA    0xCD     CALL 0x02B7
        # 0x02B7    0xF5     PUSH AF <-- A write occurs (Wait for 3 more cycles)
        # 0x02B8    0xFE     CP A,0x0A
        # 0x02BA    0xC4     CALL NZ,0x026A
        # 0x026A    0xF5     PUSH AF <-- Another write occurs, but the previous one hasn't finished!

        if self._cycles % 4 == 0:
            # RAM is 1Mhz (every 4 cycles)
            self._memory.Tick()

        if self._cycles % 2 == 0:
            # VRAM is 2Mhz (every 2 cycles)
            self._memory.TickVRAM()

        if self._cycles % 67000 == 0:
            # LCD refreshes @ 59.7Hz
            # self._lcd.Tick()
            pass

        # Can't get spec on audio, but it should be 4MHz
        #self._audio.Tick()

        # Clock, PPU and CPU tick @ 4MHz
        self._tick_timers()
        #self._ppu.Tick()
        self._cpu.Tick()
        self._cycles += 1

    def TickForever(self):
        """Ticks until an explicit stop is made"""

        self._is_ticking = True
        while(self._should_run):
            start = time.monotonic()
            self.Tick()
            end = time.monotonic()
            self._time += (end-start)
        #end While
        self._is_ticking = False

        # if we exited the loop for any reason, prime it for the next run
        self._should_run = True
    #end Tick
#end class