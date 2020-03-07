import time

class Clock:
    """
    Emulates the System master clock by subdividing the machine cycle @ 4MHz
    """

    def __init__(self, cpu, memory, video, audio):
        self._cpu = cpu
        self._memory = memory
        self._video = video
        self._audio = audio

        self._cycles = 0
        self._time = 0
        self._should_run = True
    #end

    def Tick(self):
        # TODO: implement clock timers
        pass

    def TickForever(self):
        """Ticks until an explicit stop is made"""
        while(self._should_run):
            start = time.monotonic()
            # We divide out main loop among the components
            # Keep in mind the timings and the order

            if self._cycles % 4 == 0:
                # RAM is 1Mhz (every 4 cycles)
                self._memory.Tick()

            if self._cycles % 2 == 0:
                # VRAM is 2Mhz (every 2 cycles)
                self._memory.TickVRAM()

            if self._cycles % 67000 == 0:
                # LCD refreshes at a rate of 59.7Hz
                # self._video.Tick()
                pass

            # Can't get spec on audio, but it should be 4MHz
            #self._audio.Tick()

            self.Tick()
            self._cpu.Tick()
            end = time.monotonic()
            self._cycles += 1
            self._time += (end-start)
        #end While

        # if we exited the loop for any reason, prime it for the next run
        self._should_run = True
    #end Tick
#end class