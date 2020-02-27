from src.cpu import CPU
from src.memory import MemoryBus
from src.instructions import *

def main():
    bus = MemoryBus()
    cpu = CPU(bus)

    val = cpu.SP = 0xfffe
    cpu.BC = 0xbeef
    assert(cpu.BC == 0xbeef)
    print(bus.ReadWorkRAM(cpu.SP, 1))
    cpu.executeArbitraryInstruction("PUSH BC")

    cpu.BC = 0xc0fe
    print(bus.ReadWorkRAM(cpu.SP, 2))
    cpu.executeArbitraryInstruction("PUSH BC")

    print(bus.ReadWorkRAM(cpu.SP, 4))
    cpu.executeArbitraryInstruction("LD BC,d16")
    assert(cpu.BC == 0x0)

    cpu.executeArbitraryInstruction("POP BC")
    print(bus.ReadWorkRAM(cpu.SP, 2))
    cpu.executeArbitraryInstruction("POP BC")
    print(bus.ReadWorkRAM(cpu.SP, 1))

    assert(cpu.BC == 0xbeef)
#end

if __name__ == "__main__":
    main()