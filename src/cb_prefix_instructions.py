from .cpu_types import *
from .instructions import *

# The list below is every single opcode that we know is needed for emulating Game Boy
# Most of the info below was compiled from the very useful opcode sheet below
#  https://www.pastraiser.com/cpu/gameboy/gameboy_opcodes.html
# Trying to read through this list is rather impossible, so searching by opcode or mnemonic is your best bet.

cb_prefix = [
    Instruction(
        0x00, "RLC B", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.B, 1), Operand.reg(Registers.B, 1) ),
        executor = RotateLeftWithCarry),
        
    Instruction(
        0x01, "RLC C", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.C, 1), Operand.reg(Registers.C, 1) ),
        executor = RotateLeftWithCarry),
        
    Instruction(
        0x02, "RLC D", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.D, 1), Operand.reg(Registers.D, 1) ),
        executor = RotateLeftWithCarry),
        
    Instruction(
        0x03, "RLC E", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.E, 1), Operand.reg(Registers.E, 1) ),
        executor = RotateLeftWithCarry),
        
    Instruction(
        0x04, "RLC H", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.H, 1), Operand.reg(Registers.H, 1) ),
        executor = RotateLeftWithCarry),
        
    Instruction(
        0x05, "RLC L", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.L, 1), Operand.reg(Registers.L, 1) ),
        executor = RotateLeftWithCarry),
        
    Instruction(
        0x06, "RLC (HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.regi(Registers.HL, 2), Operand.regi(Registers.HL, 2) ),
        executor = RotateLeftWithCarry),
        
    Instruction(
        0x07, "RLC A", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = RotateLeftWithCarry),
        
    Instruction(
        0x08, "RRC B", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.B, 1), Operand.reg(Registers.B, 1) ),
        executor = RotateRightWithCarry),
        
    Instruction(
        0x09, "RRC C", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.C, 1), Operand.reg(Registers.C, 1) ),
        executor = RotateRightWithCarry),
        
    Instruction(
        0x0A, "RRC D", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.D, 1), Operand.reg(Registers.D, 1) ),
        executor = RotateRightWithCarry),
        
    Instruction(
        0x0B, "RRC E", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.E, 1), Operand.reg(Registers.E, 1) ),
        executor = RotateRightWithCarry),
        
    Instruction(
        0x0C, "RRC H", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.H, 1), Operand.reg(Registers.H, 1) ),
        executor = RotateRightWithCarry),
        
    Instruction(
        0x0D, "RRC L", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.L, 1), Operand.reg(Registers.L, 1) ),
        executor = RotateRightWithCarry),
        
    Instruction(
        0x0E, "RRC (HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.regi(Registers.HL, 2), Operand.regi(Registers.HL, 2) ),
        executor = RotateRightWithCarry),
        
    Instruction(
        0x0F, "RRC A", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = RotateRightWithCarry),
        
    Instruction(
        0x10, "RL B", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.B, 1), Operand.reg(Registers.B, 1) ),
        executor = RotateLeft),
        
    Instruction(
        0x11, "RL C", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.C, 1), Operand.reg(Registers.C, 1) ),
        executor = RotateLeft),
        
    Instruction(
        0x12, "RL D", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.D, 1), Operand.reg(Registers.D, 1) ),
        executor = RotateLeft),
        
    Instruction(
        0x13, "RL E", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.E, 1), Operand.reg(Registers.E, 1) ),
        executor = RotateLeft),
        
    Instruction(
        0x14, "RL H", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.H, 1), Operand.reg(Registers.H, 1) ),
        executor = RotateLeft),
        
    Instruction(
        0x15, "RL L", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.L, 1), Operand.reg(Registers.L, 1) ),
        executor = RotateLeft),
        
    Instruction(
        0x16, "RL (HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.regi(Registers.HL, 2), Operand.regi(Registers.HL, 2) ),
        executor = RotateLeft),
        
    Instruction(
        0x17, "RL A", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = RotateLeft),
        
    Instruction(
        0x18, "RR B", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.B, 1), Operand.reg(Registers.B, 1) ),
        executor = RotateRight),
        
    Instruction(
        0x19, "RR C", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.C, 1), Operand.reg(Registers.C, 1) ),
        executor = RotateRight),
        
    Instruction(
        0x1A, "RR D", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.D, 1), Operand.reg(Registers.D, 1) ),
        executor = RotateRight),
        
    Instruction(
        0x1B, "RR E", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.E, 1), Operand.reg(Registers.E, 1) ),
        executor = RotateRight),
        
    Instruction(
        0x1C, "RR H", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.H, 1), Operand.reg(Registers.H, 1) ),
        executor = RotateRight),
        
    Instruction(
        0x1D, "RR L", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.L, 1), Operand.reg(Registers.L, 1) ),
        executor = RotateRight),
        
    Instruction(
        0x1E, "RR (HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.regi(Registers.HL, 2), Operand.regi(Registers.HL, 2) ),
        executor = RotateRight),
        
    Instruction(
        0x1F, "RR A", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = RotateRight),
        
    Instruction(
        0x20, "SLA B", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.B, 1), Operand.reg(Registers.B, 1) ),
        executor = ShiftLeft),
        
    Instruction(
        0x21, "SLA C", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.C, 1), Operand.reg(Registers.C, 1) ),
        executor = ShiftLeft),
        
    Instruction(
        0x22, "SLA D", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.D, 1), Operand.reg(Registers.D, 1) ),
        executor = ShiftLeft),
        
    Instruction(
        0x23, "SLA E", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.E, 1), Operand.reg(Registers.E, 1) ),
        executor = ShiftLeft),
        
    Instruction(
        0x24, "SLA H", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.H, 1), Operand.reg(Registers.H, 1) ),
        executor = ShiftLeft),
        
    Instruction(
        0x25, "SLA L", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.L, 1), Operand.reg(Registers.L, 1) ),
        executor = ShiftLeft),
        
    Instruction(
        0x26, "SLA (HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.regi(Registers.HL, 2), Operand.regi(Registers.HL, 2) ),
        executor = ShiftLeft),
        
    Instruction(
        0x27, "SLA A", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = ShiftLeft),
        
    Instruction(
        0x28, "SRA B", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.B, 1), Operand.reg(Registers.B, 1) ),
        executor = ShiftRightArithmetic),
        
    Instruction(
        0x29, "SRA C", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.C, 1), Operand.reg(Registers.C, 1) ),
        executor = ShiftRightArithmetic),
        
    Instruction(
        0x2A, "SRA D", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.D, 1), Operand.reg(Registers.D, 1) ),
        executor = ShiftRightArithmetic),
        
    Instruction(
        0x2B, "SRA E", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.E, 1), Operand.reg(Registers.E, 1) ),
        executor = ShiftRightArithmetic),
        
    Instruction(
        0x2C, "SRA H", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.H, 1), Operand.reg(Registers.H, 1) ),
        executor = ShiftRightArithmetic),
        
    Instruction(
        0x2D, "SRA L", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.L, 1), Operand.reg(Registers.L, 1) ),
        executor = ShiftRightArithmetic),
        
    Instruction(
        0x2E, "SRA (HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.regi(Registers.HL, 2), Operand.regi(Registers.HL, 2) ),
        executor = ShiftRightArithmetic),
        
    Instruction(
        0x2F, "SRA A", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = ShiftRightArithmetic),
        
    Instruction(
        0x30, "SWAP B", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.B, 1), Operand.reg(Registers.B, 1) ),
        executor = None),
        
    Instruction(
        0x31, "SWAP C", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.C, 1), Operand.reg(Registers.C, 1) ),
        executor = None),
        
    Instruction(
        0x32, "SWAP D", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.D, 1), Operand.reg(Registers.D, 1) ),
        executor = None),
        
    Instruction(
        0x33, "SWAP E", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.E, 1), Operand.reg(Registers.E, 1) ),
        executor = None),
        
    Instruction(
        0x34, "SWAP H", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.H, 1), Operand.reg(Registers.H, 1) ),
        executor = None),
        
    Instruction(
        0x35, "SWAP L", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.L, 1), Operand.reg(Registers.L, 1) ),
        executor = None),
        
    Instruction(
        0x36, "SWAP (HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.regi(Registers.HL, 2), Operand.regi(Registers.HL, 2) ),
        executor = None),
        
    Instruction(
        0x37, "SWAP A", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = None),
        
    Instruction(
        0x38, "SRL B", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.B, 1), Operand.reg(Registers.B, 1) ),
        executor = ShiftRight),
        
    Instruction(
        0x39, "SRL C", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.C, 1), Operand.reg(Registers.C, 1) ),
        executor = ShiftRight),
        
    Instruction(
        0x3A, "SRL D", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.D, 1), Operand.reg(Registers.D, 1) ),
        executor = ShiftRight),
        
    Instruction(
        0x3B, "SRL E", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.E, 1), Operand.reg(Registers.E, 1) ),
        executor = ShiftRight),
        
    Instruction(
        0x3C, "SRL H", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.H, 1), Operand.reg(Registers.H, 1) ),
        executor = ShiftRight),
        
    Instruction(
        0x3D, "SRL L", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.L, 1), Operand.reg(Registers.L, 1) ),
        executor = ShiftRight),
        
    Instruction(
        0x3E, "SRL (HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.regi(Registers.HL, 2), Operand.regi(Registers.HL, 2) ),
        executor = ShiftRight),
        
    Instruction(
        0x3F, "SRL A", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = ShiftRight),
        
    Instruction(
        0x40, "BIT 0,B", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(0), Operand.reg(Registers.B, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x41, "BIT 0,C", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(0), Operand.reg(Registers.C, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x42, "BIT 0,D", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(0), Operand.reg(Registers.D, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x43, "BIT 0,E", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(0), Operand.reg(Registers.E, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x44, "BIT 0,H", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(0), Operand.reg(Registers.H, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x45, "BIT 0,L", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(0), Operand.reg(Registers.L, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x46, "BIT 0,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(0), Operand.regi(Registers.HL, 2) ),
        executor = CheckBit),
        
    Instruction(
        0x47, "BIT 0,A", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(0), Operand.reg(Registers.A, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x48, "BIT 1,B", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(1), Operand.reg(Registers.B, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x49, "BIT 1,C", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(1), Operand.reg(Registers.C, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x4A, "BIT 1,D", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(1), Operand.reg(Registers.D, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x4B, "BIT 1,E", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(1), Operand.reg(Registers.E, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x4C, "BIT 1,H", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(1), Operand.reg(Registers.H, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x4D, "BIT 1,L", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(1), Operand.reg(Registers.L, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x4E, "BIT 1,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(1), Operand.regi(Registers.HL, 2) ),
        executor = CheckBit),
        
    Instruction(
        0x4F, "BIT 1,A", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(1), Operand.reg(Registers.A, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x50, "BIT 2,B", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(2), Operand.reg(Registers.B, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x51, "BIT 2,C", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(2), Operand.reg(Registers.C, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x52, "BIT 2,D", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(2), Operand.reg(Registers.D, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x53, "BIT 2,E", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(2), Operand.reg(Registers.E, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x54, "BIT 2,H", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(2), Operand.reg(Registers.H, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x55, "BIT 2,L", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(2), Operand.reg(Registers.L, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x56, "BIT 2,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(2), Operand.regi(Registers.HL, 2) ),
        executor = CheckBit),
        
    Instruction(
        0x57, "BIT 2,A", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(2), Operand.reg(Registers.A, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x58, "BIT 3,B", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(3), Operand.reg(Registers.B, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x59, "BIT 3,C", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(3), Operand.reg(Registers.C, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x5A, "BIT 3,D", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(3), Operand.reg(Registers.D, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x5B, "BIT 3,E", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(3), Operand.reg(Registers.E, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x5C, "BIT 3,H", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(3), Operand.reg(Registers.H, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x5D, "BIT 3,L", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(3), Operand.reg(Registers.L, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x5E, "BIT 3,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(3), Operand.regi(Registers.HL, 2) ),
        executor = CheckBit),
        
    Instruction(
        0x5F, "BIT 3,A", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(3), Operand.reg(Registers.A, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x60, "BIT 4,B", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(4), Operand.reg(Registers.B, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x61, "BIT 4,C", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(4), Operand.reg(Registers.C, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x62, "BIT 4,D", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(4), Operand.reg(Registers.D, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x63, "BIT 4,E", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(4), Operand.reg(Registers.E, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x64, "BIT 4,H", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(4), Operand.reg(Registers.H, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x65, "BIT 4,L", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(4), Operand.reg(Registers.L, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x66, "BIT 4,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(4), Operand.regi(Registers.HL, 2) ),
        executor = CheckBit),
        
    Instruction(
        0x67, "BIT 4,A", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(4), Operand.reg(Registers.A, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x68, "BIT 5,B", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(5), Operand.reg(Registers.B, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x69, "BIT 5,C", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(5), Operand.reg(Registers.C, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x6A, "BIT 5,D", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(5), Operand.reg(Registers.D, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x6B, "BIT 5,E", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(5), Operand.reg(Registers.E, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x6C, "BIT 5,H", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(5), Operand.reg(Registers.H, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x6D, "BIT 5,L", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(5), Operand.reg(Registers.L, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x6E, "BIT 5,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(5), Operand.regi(Registers.HL, 2) ),
        executor = CheckBit),
        
    Instruction(
        0x6F, "BIT 5,A", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(5), Operand.reg(Registers.A, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x70, "BIT 6,B", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(6), Operand.reg(Registers.B, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x71, "BIT 6,C", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(6), Operand.reg(Registers.C, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x72, "BIT 6,D", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(6), Operand.reg(Registers.D, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x73, "BIT 6,E", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(6), Operand.reg(Registers.E, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x74, "BIT 6,H", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(6), Operand.reg(Registers.H, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x75, "BIT 6,L", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(6), Operand.reg(Registers.L, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x76, "BIT 6,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(6), Operand.regi(Registers.HL, 2) ),
        executor = CheckBit),
        
    Instruction(
        0x77, "BIT 6,A", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(6), Operand.reg(Registers.A, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x78, "BIT 7,B", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(7), Operand.reg(Registers.B, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x79, "BIT 7,C", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(7), Operand.reg(Registers.C, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x7A, "BIT 7,D", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(7), Operand.reg(Registers.D, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x7B, "BIT 7,E", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(7), Operand.reg(Registers.E, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x7C, "BIT 7,H", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(7), Operand.reg(Registers.H, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x7D, "BIT 7,L", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(7), Operand.reg(Registers.L, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x7E, "BIT 7,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(7), Operand.regi(Registers.HL, 2) ),
        executor = CheckBit),
        
    Instruction(
        0x7F, "BIT 7,A", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = ( Operand.const(7), Operand.reg(Registers.A, 1) ),
        executor = CheckBit),
        
    Instruction(
        0x80, "RES 0,B", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(0), Operand.reg(Registers.B, 1) ),
        executor = Reset),
        
    Instruction(
        0x81, "RES 0,C", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(0), Operand.reg(Registers.C, 1) ),
        executor = Reset),
        
    Instruction(
        0x82, "RES 0,D", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(0), Operand.reg(Registers.D, 1) ),
        executor = Reset),
        
    Instruction(
        0x83, "RES 0,E", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(0), Operand.reg(Registers.E, 1) ),
        executor = Reset),
        
    Instruction(
        0x84, "RES 0,H", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(0), Operand.reg(Registers.H, 1) ),
        executor = Reset),
        
    Instruction(
        0x85, "RES 0,L", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(0), Operand.reg(Registers.L, 1) ),
        executor = Reset),
        
    Instruction(
        0x86, "RES 0,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags=None,
        operands = ( Operand.const(0), Operand.regi(Registers.HL, 2) ),
        executor = Reset),
        
    Instruction(
        0x87, "RES 0,A", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(0), Operand.reg(Registers.A, 1) ),
        executor = Reset),
        
    Instruction(
        0x88, "RES 1,B", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(1), Operand.reg(Registers.B, 1) ),
        executor = Reset),
        
    Instruction(
        0x89, "RES 1,C", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(1), Operand.reg(Registers.C, 1) ),
        executor = Reset),
        
    Instruction(
        0x8A, "RES 1,D", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(1), Operand.reg(Registers.D, 1) ),
        executor = Reset),
        
    Instruction(
        0x8B, "RES 1,E", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(1), Operand.reg(Registers.E, 1) ),
        executor = Reset),
        
    Instruction(
        0x8C, "RES 1,H", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(1), Operand.reg(Registers.H, 1) ),
        executor = Reset),
        
    Instruction(
        0x8D, "RES 1,L", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(1), Operand.reg(Registers.L, 1) ),
        executor = Reset),
        
    Instruction(
        0x8E, "RES 1,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags=None,
        operands = ( Operand.const(1), Operand.regi(Registers.HL, 2) ),
        executor = Reset),
        
    Instruction(
        0x8F, "RES 1,A", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(1), Operand.reg(Registers.A, 1) ),
        executor = Reset),
        
    Instruction(
        0x90, "RES 2,B", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(2), Operand.reg(Registers.B, 1) ),
        executor = Reset),
        
    Instruction(
        0x91, "RES 2,C", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(2), Operand.reg(Registers.C, 1) ),
        executor = Reset),
        
    Instruction(
        0x92, "RES 2,D", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(2), Operand.reg(Registers.D, 1) ),
        executor = Reset),
        
    Instruction(
        0x93, "RES 2,E", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(2), Operand.reg(Registers.E, 1) ),
        executor = Reset),
        
    Instruction(
        0x94, "RES 2,H", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(2), Operand.reg(Registers.H, 1) ),
        executor = Reset),
        
    Instruction(
        0x95, "RES 2,L", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(2), Operand.reg(Registers.L, 1) ),
        executor = Reset),
        
    Instruction(
        0x96, "RES 2,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags=None,
        operands = ( Operand.const(2), Operand.regi(Registers.HL, 2) ),
        executor = Reset),
        
    Instruction(
        0x97, "RES 2,A", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(2), Operand.reg(Registers.A, 1) ),
        executor = Reset),
        
    Instruction(
        0x98, "RES 3,B", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(3), Operand.reg(Registers.B, 1) ),
        executor = Reset),
        
    Instruction(
        0x99, "RES 3,C", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(3), Operand.reg(Registers.C, 1) ),
        executor = Reset),
        
    Instruction(
        0x9A, "RES 3,D", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(3), Operand.reg(Registers.D, 1) ),
        executor = Reset),
        
    Instruction(
        0x9B, "RES 3,E", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(3), Operand.reg(Registers.E, 1) ),
        executor = Reset),
        
    Instruction(
        0x9C, "RES 3,H", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(3), Operand.reg(Registers.H, 1) ),
        executor = Reset),
        
    Instruction(
        0x9D, "RES 3,L", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(3), Operand.reg(Registers.L, 1) ),
        executor = Reset),
        
    Instruction(
        0x9E, "RES 3,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags=None,
        operands = ( Operand.const(3), Operand.regi(Registers.HL, 2) ),
        executor = Reset),
        
    Instruction(
        0x9F, "RES 3,A", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(3), Operand.reg(Registers.A, 1) ),
        executor = Reset),
        
    Instruction(
        0xA0, "RES 4,B", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(4), Operand.reg(Registers.B, 1) ),
        executor = Reset),
        
    Instruction(
        0xA1, "RES 4,C", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(4), Operand.reg(Registers.C, 1) ),
        executor = Reset),
        
    Instruction(
        0xA2, "RES 4,D", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(4), Operand.reg(Registers.D, 1) ),
        executor = Reset),
        
    Instruction(
        0xA3, "RES 4,E", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(4), Operand.reg(Registers.E, 1) ),
        executor = Reset),
        
    Instruction(
        0xA4, "RES 4,H", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(4), Operand.reg(Registers.H, 1) ),
        executor = Reset),
        
    Instruction(
        0xA5, "RES 4,L", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(4), Operand.reg(Registers.L, 1) ),
        executor = Reset),
        
    Instruction(
        0xA6, "RES 4,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags=None,
        operands = ( Operand.const(4), Operand.regi(Registers.HL, 2) ),
        executor = Reset),
        
    Instruction(
        0xA7, "RES 4,A", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(4), Operand.reg(Registers.A, 1) ),
        executor = Reset),
        
    Instruction(
        0xA8, "RES 5,B", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(5), Operand.reg(Registers.B, 1) ),
        executor = Reset),
        
    Instruction(
        0xA9, "RES 5,C", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(5), Operand.reg(Registers.C, 1) ),
        executor = Reset),
        
    Instruction(
        0xAA, "RES 5,D", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(5), Operand.reg(Registers.D, 1) ),
        executor = Reset),
        
    Instruction(
        0xAB, "RES 5,E", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(5), Operand.reg(Registers.E, 1) ),
        executor = Reset),
        
    Instruction(
        0xAC, "RES 5,H", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(5), Operand.reg(Registers.H, 1) ),
        executor = Reset),
        
    Instruction(
        0xAD, "RES 5,L", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(5), Operand.reg(Registers.L, 1) ),
        executor = Reset),
        
    Instruction(
        0xAE, "RES 5,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags=None,
        operands = ( Operand.const(5), Operand.regi(Registers.HL, 2) ),
        executor = Reset),
        
    Instruction(
        0xAF, "RES 5,A", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(5), Operand.reg(Registers.A, 1) ),
        executor = Reset),
        
    Instruction(
        0xB0, "RES 6,B", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(6), Operand.reg(Registers.B, 1) ),
        executor = Reset),
        
    Instruction(
        0xB1, "RES 6,C", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(6), Operand.reg(Registers.C, 1) ),
        executor = Reset),
        
    Instruction(
        0xB2, "RES 6,D", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(6), Operand.reg(Registers.D, 1) ),
        executor = Reset),
        
    Instruction(
        0xB3, "RES 6,E", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(6), Operand.reg(Registers.E, 1) ),
        executor = Reset),
        
    Instruction(
        0xB4, "RES 6,H", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(6), Operand.reg(Registers.H, 1) ),
        executor = Reset),
        
    Instruction(
        0xB5, "RES 6,L", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(6), Operand.reg(Registers.L, 1) ),
        executor = Reset),
        
    Instruction(
        0xB6, "RES 6,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags=None,
        operands = ( Operand.const(6), Operand.regi(Registers.HL, 2) ),
        executor = Reset),
        
    Instruction(
        0xB7, "RES 6,A", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(6), Operand.reg(Registers.A, 1) ),
        executor = Reset),
        
    Instruction(
        0xB8, "RES 7,B", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(7), Operand.reg(Registers.B, 1) ),
        executor = Reset),
        
    Instruction(
        0xB9, "RES 7,C", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(7), Operand.reg(Registers.C, 1) ),
        executor = Reset),
        
    Instruction(
        0xBA, "RES 7,D", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(7), Operand.reg(Registers.D, 1) ),
        executor = Reset),
        
    Instruction(
        0xBB, "RES 7,E", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(7), Operand.reg(Registers.E, 1) ),
        executor = Reset),
        
    Instruction(
        0xBC, "RES 7,H", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(7), Operand.reg(Registers.H, 1) ),
        executor = Reset),
        
    Instruction(
        0xBD, "RES 7,L", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(7), Operand.reg(Registers.L, 1) ),
        executor = Reset),
        
    Instruction(
        0xBE, "RES 7,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags=None,
        operands = ( Operand.const(7), Operand.regi(Registers.HL, 2) ),
        executor = Reset),
        
    Instruction(
        0xBF, "RES 7,A", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.const(7), Operand.reg(Registers.A, 1) ),
        executor = Reset),
        
    Instruction(
        0xC0, "SET 0,B", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.B, 1), Operand.const(0) ),
        executor = SetBit),
        
    Instruction(
        0xC1, "SET 0,C", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.const(0) ),
        executor = SetBit),
        
    Instruction(
        0xC2, "SET 0,D", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.D, 1), Operand.const(0) ),
        executor = SetBit),
        
    Instruction(
        0xC3, "SET 0,E", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.E, 1), Operand.const(0) ),
        executor = SetBit),
        
    Instruction(
        0xC4, "SET 0,H", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.H, 1), Operand.const(0) ),
        executor = SetBit),
        
    Instruction(
        0xC5, "SET 0,L", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.L, 1), Operand.const(0) ),
        executor = SetBit),
        
    Instruction(
        0xC6, "SET 0,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags=None,
        operands = ( Operand.regi(Registers.HL, 2), Operand.const(0) ),
        executor = SetBit),
        
    Instruction(
        0xC7, "SET 0,A", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.const(0) ),
        executor = SetBit),
        
    Instruction(
        0xC8, "SET 1,B", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.B, 1), Operand.const(1) ),
        executor = SetBit),
        
    Instruction(
        0xC9, "SET 1,C", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.const(1) ),
        executor = SetBit),
        
    Instruction(
        0xCA, "SET 1,D", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.D, 1), Operand.const(1) ),
        executor = SetBit),
        
    Instruction(
        0xCB, "SET 1,E", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.E, 1), Operand.const(1) ),
        executor = SetBit),
        
    Instruction(
        0xCC, "SET 1,H", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.H, 1), Operand.const(1) ),
        executor = SetBit),
        
    Instruction(
        0xCD, "SET 1,L", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.L, 1), Operand.const(1) ),
        executor = SetBit),
        
    Instruction(
        0xCE, "SET 1,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags=None,
        operands = ( Operand.regi(Registers.HL, 2), Operand.const(1) ),
        executor = SetBit),
        
    Instruction(
        0xCF, "SET 1,A", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.const(1) ),
        executor = SetBit),
        
    Instruction(
        0xD0, "SET 2,B", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.B, 1), Operand.const(2) ),
        executor = SetBit),
        
    Instruction(
        0xD1, "SET 2,C", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.const(2) ),
        executor = SetBit),
        
    Instruction(
        0xD2, "SET 2,D", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.D, 1), Operand.const(2) ),
        executor = SetBit),
        
    Instruction(
        0xD3, "SET 2,E", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.E, 1), Operand.const(2) ),
        executor = SetBit),
        
    Instruction(
        0xD4, "SET 2,H", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.H, 1), Operand.const(2) ),
        executor = SetBit),
        
    Instruction(
        0xD5, "SET 2,L", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.L, 1), Operand.const(2) ),
        executor = SetBit),
        
    Instruction(
        0xD6, "SET 2,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags=None,
        operands = ( Operand.regi(Registers.HL, 2), Operand.const(2) ),
        executor = SetBit),
        
    Instruction(
        0xD7, "SET 2,A", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.const(2) ),
        executor = SetBit),
        
    Instruction(
        0xD8, "SET 3,B", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.B, 1), Operand.const(3) ),
        executor = SetBit),
        
    Instruction(
        0xD9, "SET 3,C", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.const(3) ),
        executor = SetBit),
        
    Instruction(
        0xDA, "SET 3,D", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.D, 1), Operand.const(3) ),
        executor = SetBit),
        
    Instruction(
        0xDB, "SET 3,E", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.E, 1), Operand.const(3) ),
        executor = SetBit),
        
    Instruction(
        0xDC, "SET 3,H", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.H, 1), Operand.const(3) ),
        executor = SetBit),
        
    Instruction(
        0xDD, "SET 3,L", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.L, 1), Operand.const(3) ),
        executor = SetBit),
        
    Instruction(
        0xDE, "SET 3,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags=None,
        operands = ( Operand.regi(Registers.HL, 2), Operand.const(3) ),
        executor = SetBit),
        
    Instruction(
        0xDF, "SET 3,A", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.const(3) ),
        executor = SetBit),
        
    Instruction(
        0xE0, "SET 4,B", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.B, 1), Operand.const(4) ),
        executor = SetBit),
        
    Instruction(
        0xE1, "SET 4,C", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.const(4) ),
        executor = SetBit),
        
    Instruction(
        0xE2, "SET 4,D", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.D, 1), Operand.const(4) ),
        executor = SetBit),
        
    Instruction(
        0xE3, "SET 4,E", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.E, 1), Operand.const(4) ),
        executor = SetBit),
        
    Instruction(
        0xE4, "SET 4,H", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.H, 1), Operand.const(4) ),
        executor = SetBit),
        
    Instruction(
        0xE5, "SET 4,L", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.L, 1), Operand.const(4) ),
        executor = SetBit),
        
    Instruction(
        0xE6, "SET 4,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags=None,
        operands = ( Operand.regi(Registers.HL, 2), Operand.const(4) ),
        executor = SetBit),
        
    Instruction(
        0xE7, "SET 4,A", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.const(4) ),
        executor = SetBit),
        
    Instruction(
        0xE8, "SET 5,B", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.B, 1), Operand.const(5) ),
        executor = SetBit),
        
    Instruction(
        0xE9, "SET 5,C", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.const(5) ),
        executor = SetBit),
        
    Instruction(
        0xEA, "SET 5,D", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.D, 1), Operand.const(5) ),
        executor = SetBit),
        
    Instruction(
        0xEB, "SET 5,E", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.E, 1), Operand.const(5) ),
        executor = SetBit),
        
    Instruction(
        0xEC, "SET 5,H", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.H, 1), Operand.const(5) ),
        executor = SetBit),
        
    Instruction(
        0xED, "SET 5,L", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.L, 1), Operand.const(5) ),
        executor = SetBit),
        
    Instruction(
        0xEE, "SET 5,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags=None,
        operands = ( Operand.regi(Registers.HL, 2), Operand.const(5) ),
        executor = SetBit),
        
    Instruction(
        0xEF, "SET 5,A", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.const(5) ),
        executor = SetBit),
        
    Instruction(
        0xF0, "SET 6,B", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.B, 1), Operand.const(6) ),
        executor = SetBit),
        
    Instruction(
        0xF1, "SET 6,C", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.const(6) ),
        executor = SetBit),
        
    Instruction(
        0xF2, "SET 6,D", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.D, 1), Operand.const(6) ),
        executor = SetBit),
        
    Instruction(
        0xF3, "SET 6,E", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.E, 1), Operand.const(6) ),
        executor = SetBit),
        
    Instruction(
        0xF4, "SET 6,H", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.H, 1), Operand.const(6) ),
        executor = SetBit),
        
    Instruction(
        0xF5, "SET 6,L", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.L, 1), Operand.const(6) ),
        executor = SetBit),
        
    Instruction(
        0xF6, "SET 6,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags=None,
        operands = ( Operand.regi(Registers.HL, 2), Operand.const(6) ),
        executor = SetBit),
        
    Instruction(
        0xF7, "SET 6,A", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.const(6) ),
        executor = SetBit),
        
    Instruction(
        0xF8, "SET 7,B", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.B, 1), Operand.const(7) ),
        executor = SetBit),
        
    Instruction(
        0xF9, "SET 7,C", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.const(7) ),
        executor = SetBit),
        
    Instruction(
        0xFA, "SET 7,D", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.D, 1), Operand.const(7) ),
        executor = SetBit),
        
    Instruction(
        0xFB, "SET 7,E", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.E, 1), Operand.const(7) ),
        executor = SetBit),
        
    Instruction(
        0xFC, "SET 7,H", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.H, 1), Operand.const(7) ),
        executor = SetBit),
        
    Instruction(
        0xFD, "SET 7,L", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.L, 1), Operand.const(7) ),
        executor = SetBit),
        
    Instruction(
        0xFE, "SET 7,(HL)", bus_width=1,
        byte_size=2, cycles=16,
        flags=None,
        operands = ( Operand.regi(Registers.HL, 2), Operand.const(7) ),
        executor = SetBit),
        
    Instruction(
        0xFF, "SET 7,A", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.const(7) ),
        executor = SetBit),
        
]

