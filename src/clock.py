
class Clock:
    def __init__(self, cpu, memory, video, audio):
        self._cpu = cpu
        self._memory = memory
        self._video = video
        self._audio = audio

        self._cycles = 0
        self._should_run = True
    #end

    def TickForever(self):
        """Ticks until an explicit stop is made"""
        while(self._should_run):
            # We divide out main loop among the components
            # Keep in mind the timings and the order

            if self._cycles % 4 == 0:
                # RAM is 1Mhz (every 4 cycles)
                self._memory.Tick()

            if self._cycles % 2 == 0:
                # VRAM is 2Mhz (every 2 cycles)
                self._memory.TickVRAM()

            # Can't get spec on audio, but it should be 4MHz
            #self._audio.Tick()

            self._cpu.Tick()
            self._cycles += 1
        #end While

        # if we exited the loop for any reason, prime it for the next run
        self._should_run = True
    #end