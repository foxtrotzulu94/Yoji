from .cpu import CPU
from .memory import Memory
from .clock import Clock

class GameBoy:
    def __init__(self):
        self._memory = Memory(synchronized = True)
        self._cpu = CPU(self._memory)
        self._audio = None
        self._video = None

        self._clock = Clock(self._cpu, self._memory, self._video, self._audio)

        self.__debug = False
    #end

    @property
    def Debug(self):
        """ Debug mode to print instructions on each tick """
        return self.__debug

    @Debug.setter
    def Debug(self, value):
        self._cpu.Debug = self.__debug = value

    def Run(self):
        """ Starts the GameBoy """
        self._clock.TickForever()