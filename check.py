from src.cpu import CPU
from src.memory import MemoryBus
from src.instructions import *

def main():
    bus = MemoryBus()
    cpu = CPU(bus)

    cpu.SP = 0xfffe
    cpu.BC = 0xbeef
    cpu.executeArbitraryInstruction("PUSH BC")
    cpu.BC = 0xc0fe
    cpu.executeArbitraryInstruction("POP BC")

    assert(cpu.BC)
#end

if __name__ == "__main__":
    main()