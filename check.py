from src.cpu import CPU
from src.memory import Memory
from src.instructions import *

def main():
    mem = Memory()
    cpu = CPU(mem)

    cpu.H = 0xED
    cpu.executeArbitraryInstruction("SWAP H")
    assert(cpu.H == 0xDE)

    cpu.executeArbitraryInstruction("CCF")
    assert(cpu.c)
    cpu.executeArbitraryInstruction("CCF")
    assert(not cpu.c)
    cpu.executeArbitraryInstruction("SCF")
    assert(cpu.c)

    val = cpu.SP = 0xfffe
    cpu.BC = 0xbeef
    assert(cpu.BC == 0xbeef)
    print(mem.Read(cpu.SP, 1))
    cpu.executeArbitraryInstruction("PUSH BC")

    cpu.BC = 0xc0fe
    print(mem.Read(cpu.SP, 2))
    cpu.executeArbitraryInstruction("PUSH BC")

    print(mem.Read(cpu.SP, 4))
    cpu.executeArbitraryInstruction("LD BC,d16")
    assert(cpu.BC == 0x0)

    cpu.executeArbitraryInstruction("POP BC")
    print(mem.Read(cpu.SP, 2))
    cpu.executeArbitraryInstruction("POP BC")
    print(mem.Read(cpu.SP, 1))

    assert(cpu.BC == 0xbeef)
#end

if __name__ == "__main__":
    main()