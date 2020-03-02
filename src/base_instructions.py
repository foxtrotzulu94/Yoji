from .cpu_types import *
from .instructions import *

# The list below is every single opcode that we know is needed for emulating Game Boy
# Most of the info below was compiled from the very useful opcode sheet below
#  https://www.pastraiser.com/cpu/gameboy/gameboy_opcodes.html
# Trying to read through this list is rather impossible, so searching by opcode or mnemonic is your best bet.

base_instructions = [
    Instruction(
        0x00, "NOP", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = None,
        executor = NoOp),
        
    Instruction(
        0x01, "LD BC,d16", bus_width=2,
        byte_size=3, cycles=12,
        flags=None,
        operands = ( Operand.reg(Registers.BC, 2), Operand.imm(2) ),
        executor = Load),
        
    Instruction(
        0x02, "LD (BC),A", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.regi(Registers.BC, 2), Operand.reg(Registers.A, 1) ),
        executor = Load),
        
    Instruction(
        0x03, "INC BC", bus_width=2,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.BC, 2), Operand.reg(Registers.BC, 2) ),
        executor = Increment),
        
    Instruction(
        0x04, "INC B", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Ignore },
        operands = ( Operand.reg(Registers.B, 1), Operand.reg(Registers.B, 1) ),
        executor = Increment),
        
    Instruction(
        0x05, "DEC B", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Ignore },
        operands = ( Operand.reg(Registers.B, 1), Operand.reg(Registers.B, 1) ),
        executor = Decrement),
        
    Instruction(
        0x06, "LD B,d8", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.B, 1), Operand.imm(1) ),
        executor = Load),
        
    Instruction(
        0x07, "RLCA", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Reset, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = RotateLeftWithCarry),
        
    Instruction(
        0x08, "LD (a16),SP", bus_width=2,
        byte_size=3, cycles=20,
        flags=None,
        operands = ( Operand.mem(2), Operand.reg(Registers.SP, 2) ),
        executor = Load),
        
    Instruction(
        0x09, "ADD HL,BC", bus_width=2,
        byte_size=1, cycles=8,
        flags={ Flag.z:Bit.Ignore, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.HL, 2), Operand.reg(Registers.BC, 2) ),
        executor = Add),
        
    Instruction(
        0x0A, "LD A,(BC)", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.regi(Registers.BC, 2) ),
        executor = Load),
        
    Instruction(
        0x0B, "DEC BC", bus_width=2,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.BC, 2), Operand.reg(Registers.BC, 2) ),
        executor = Decrement),
        
    Instruction(
        0x0C, "INC C", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Ignore },
        operands = ( Operand.reg(Registers.C, 1), Operand.reg(Registers.C, 1) ),
        executor = Increment),
        
    Instruction(
        0x0D, "DEC C", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Ignore },
        operands = ( Operand.reg(Registers.C, 1), Operand.reg(Registers.C, 1) ),
        executor = Decrement),
        
    Instruction(
        0x0E, "LD C,d8", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.imm(1) ),
        executor = Load),
        
    Instruction(
        0x0F, "RRCA", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Reset, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = None,
        executor = RotateRightWithCarry),
        
    Instruction(
        0x10, "STOP", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = None,
        executor = Stop),
        
    Instruction(
        0x11, "LD DE,d16", bus_width=2,
        byte_size=3, cycles=12,
        flags=None,
        operands = ( Operand.reg(Registers.DE, 2), Operand.imm(2) ),
        executor = Load),
        
    Instruction(
        0x12, "LD (DE),A", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.regi(Registers.DE, 2), Operand.reg(Registers.A, 1) ),
        executor = Load),
        
    Instruction(
        0x13, "INC DE", bus_width=2,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.DE, 2), Operand.reg(Registers.DE, 2) ),
        executor = Increment),
        
    Instruction(
        0x14, "INC D", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Ignore },
        operands = ( Operand.reg(Registers.D, 1), Operand.reg(Registers.D, 1) ),
        executor = Increment),
        
    Instruction(
        0x15, "DEC D", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Ignore },
        operands = ( Operand.reg(Registers.D, 1), Operand.reg(Registers.D, 1) ),
        executor = Decrement),
        
    Instruction(
        0x16, "LD D,d8", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.D, 1), Operand.imm(1) ),
        executor = Load),
        
    Instruction(
        0x17, "RLA", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Reset, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = RotateLeft),
        
    Instruction(
        0x18, "JR r8", bus_width=1,
        byte_size=2, cycles=12,
        flags=None,
        operands = ( None, Operand.imm(1) ),
        executor = NearJump),
        
    Instruction(
        0x19, "ADD HL,DE", bus_width=2,
        byte_size=1, cycles=8,
        flags={ Flag.z:Bit.Ignore, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.HL, 2), Operand.reg(Registers.DE, 2) ),
        executor = Add),
        
    Instruction(
        0x1A, "LD A,(DE)", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.regi(Registers.DE, 2) ),
        executor = Load),
        
    Instruction(
        0x1B, "DEC DE", bus_width=2,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.DE, 2), Operand.reg(Registers.DE, 2) ),
        executor = Decrement),
        
    Instruction(
        0x1C, "INC E", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Ignore },
        operands = ( Operand.reg(Registers.E, 1), Operand.reg(Registers.E, 1) ),
        executor = Increment),
        
    Instruction(
        0x1D, "DEC E", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Ignore },
        operands = ( Operand.reg(Registers.E, 1), Operand.reg(Registers.E, 1) ),
        executor = Decrement),
        
    Instruction(
        0x1E, "LD E,d8", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.E, 1), Operand.imm(1) ),
        executor = Load),
        
    Instruction(
        0x1F, "RRA", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Reset, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = None,
        executor = RotateRight),
        
    Instruction(
        0x20, "JR NZ,r8", bus_width=1,
        byte_size=2, cycles=12/8,
        flags=None,
        operands = ( Operand.bit(Flag.z, Bit.Reset), Operand.imm(1) ),
        executor = NearJump),
        
    Instruction(
        0x21, "LD HL,d16", bus_width=2,
        byte_size=3, cycles=12,
        flags=None,
        operands = ( Operand.reg(Registers.HL, 2), Operand.imm(2) ),
        executor = Load),
        
    Instruction(
        0x22, "LD (HL+),A", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.regInc(Registers.HL, 2), Operand.reg(Registers.A, 1) ),
        executor = Load),
        
    Instruction(
        0x23, "INC HL", bus_width=2,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.HL, 2), Operand.reg(Registers.HL, 2) ),
        executor = Increment),
        
    Instruction(
        0x24, "INC H", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Ignore },
        operands = ( Operand.reg(Registers.H, 1), Operand.reg(Registers.H, 1) ),
        executor = Increment),
        
    Instruction(
        0x25, "DEC H", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Ignore },
        operands = ( Operand.reg(Registers.H, 1), Operand.reg(Registers.H, 1) ),
        executor = Decrement),
        
    Instruction(
        0x26, "LD H,d8", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.H, 1), Operand.imm(1) ),
        executor = Load),
        
    Instruction(
        0x27, "DAA", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Ignore, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = None,
        executor = DecimalAdjustAccumulator),
        
    Instruction(
        0x28, "JR Z,r8", bus_width=1,
        byte_size=2, cycles=12/8,
        flags=None,
        operands = ( Operand.bit(Flag.z, Bit.Set), Operand.imm(1) ),
        executor = NearJump),
        
    Instruction(
        0x29, "ADD HL,HL", bus_width=2,
        byte_size=1, cycles=8,
        flags={ Flag.z:Bit.Ignore, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.HL, 2), Operand.reg(Registers.HL, 2) ),
        executor = Add),
        
    Instruction(
        0x2A, "LD A,(HL+)", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.regInc(Registers.HL, 2) ),
        executor = Load),
        
    Instruction(
        0x2B, "DEC HL", bus_width=2,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.HL, 2), Operand.reg(Registers.HL, 2) ),
        executor = Decrement),
        
    Instruction(
        0x2C, "INC L", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Ignore },
        operands = ( Operand.reg(Registers.L, 1), Operand.reg(Registers.L, 1) ),
        executor = Increment),
        
    Instruction(
        0x2D, "DEC L", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Ignore },
        operands = ( Operand.reg(Registers.L, 1), Operand.reg(Registers.L, 1) ),
        executor = Decrement),
        
    Instruction(
        0x2E, "LD L,d8", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.L, 1), Operand.imm(1) ),
        executor = Load),
        
    Instruction(
        0x2F, "CPL", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Ignore, Flag.n:Bit.Set, Flag.h:Bit.Set, Flag.c:Bit.Ignore },
        operands = None,
        executor = ComplementA),
        
    Instruction(
        0x30, "JR NC,r8", bus_width=1,
        byte_size=2, cycles=12/8,
        flags=None,
        operands = ( Operand.bit(Flag.c, Bit.Reset), Operand.imm(1) ),
        executor = NearJump),
        
    Instruction(
        0x31, "LD SP,d16", bus_width=2,
        byte_size=3, cycles=12,
        flags=None,
        operands = ( Operand.reg(Registers.SP, 2), Operand.imm(2) ),
        executor = Load),
        
    Instruction(
        0x32, "LD (HL-),A", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.regDec(Registers.HL, 2), Operand.reg(Registers.A, 1) ),
        executor = Load),
        
    Instruction(
        0x33, "INC SP", bus_width=2,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.SP, 2), Operand.reg(Registers.SP, 2) ),
        executor = Increment),
        
    Instruction(
        0x34, "INC (HL)", bus_width=1,
        byte_size=1, cycles=12,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Ignore },
        operands = ( Operand.regi(Registers.HL, 2), Operand.regi(Registers.HL, 2) ),
        executor = Increment),
        
    Instruction(
        0x35, "DEC (HL)", bus_width=1,
        byte_size=1, cycles=12,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Ignore },
        operands = ( Operand.regi(Registers.HL, 2), Operand.regi(Registers.HL, 2) ),
        executor = Decrement),
        
    Instruction(
        0x36, "LD (HL),d8", bus_width=1,
        byte_size=2, cycles=12,
        flags=None,
        operands = ( Operand.regi(Registers.HL, 2), Operand.imm(1) ),
        executor = Load),
        
    Instruction(
        0x37, "SCF", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Ignore, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Set },
        operands = None,
        executor = SetCarry),
        
    Instruction(
        0x38, "JR C,r8", bus_width=1,
        byte_size=2, cycles=12/8,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.imm(1) ),
        executor = NearJump),
        
    Instruction(
        0x39, "ADD HL,SP", bus_width=2,
        byte_size=1, cycles=8,
        flags={ Flag.z:Bit.Ignore, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.HL, 2), Operand.reg(Registers.SP, 2) ),
        executor = Add),
        
    Instruction(
        0x3A, "LD A,(HL-)", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.regDec(Registers.HL, 2) ),
        executor = Load),
        
    Instruction(
        0x3B, "DEC SP", bus_width=2,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.SP, 2), Operand.reg(Registers.SP, 2) ),
        executor = Decrement),
        
    Instruction(
        0x3C, "INC A", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Ignore },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = Increment),
        
    Instruction(
        0x3D, "DEC A", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Ignore },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = Decrement),
        
    Instruction(
        0x3E, "LD A,d8", bus_width=1,
        byte_size=2, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.imm(1) ),
        executor = Load),
        
    Instruction(
        0x3F, "CCF", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Ignore, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Calculate },
        operands = None,
        executor = InvertCarry),
        
    Instruction(
        0x40, "LD B,B", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.B, 1), Operand.reg(Registers.B, 1) ),
        executor = Load),
        
    Instruction(
        0x41, "LD B,C", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.B, 1), Operand.reg(Registers.C, 1) ),
        executor = Load),
        
    Instruction(
        0x42, "LD B,D", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.B, 1), Operand.reg(Registers.D, 1) ),
        executor = Load),
        
    Instruction(
        0x43, "LD B,E", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.B, 1), Operand.reg(Registers.E, 1) ),
        executor = Load),
        
    Instruction(
        0x44, "LD B,H", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.B, 1), Operand.reg(Registers.H, 1) ),
        executor = Load),
        
    Instruction(
        0x45, "LD B,L", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.B, 1), Operand.reg(Registers.L, 1) ),
        executor = Load),
        
    Instruction(
        0x46, "LD B,(HL)", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.B, 1), Operand.regi(Registers.HL, 2) ),
        executor = Load),
        
    Instruction(
        0x47, "LD B,A", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.B, 1), Operand.reg(Registers.A, 1) ),
        executor = Load),
        
    Instruction(
        0x48, "LD C,B", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.reg(Registers.B, 1) ),
        executor = Load),
        
    Instruction(
        0x49, "LD C,C", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.reg(Registers.C, 1) ),
        executor = Load),
        
    Instruction(
        0x4A, "LD C,D", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.reg(Registers.D, 1) ),
        executor = Load),
        
    Instruction(
        0x4B, "LD C,E", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.reg(Registers.E, 1) ),
        executor = Load),
        
    Instruction(
        0x4C, "LD C,H", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.reg(Registers.H, 1) ),
        executor = Load),
        
    Instruction(
        0x4D, "LD C,L", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.reg(Registers.L, 1) ),
        executor = Load),
        
    Instruction(
        0x4E, "LD C,(HL)", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.regi(Registers.HL, 2) ),
        executor = Load),
        
    Instruction(
        0x4F, "LD C,A", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.reg(Registers.A, 1) ),
        executor = Load),
        
    Instruction(
        0x50, "LD D,B", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.D, 1), Operand.reg(Registers.B, 1) ),
        executor = Load),
        
    Instruction(
        0x51, "LD D,C", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.D, 1), Operand.reg(Registers.C, 1) ),
        executor = Load),
        
    Instruction(
        0x52, "LD D,D", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.D, 1), Operand.reg(Registers.D, 1) ),
        executor = Load),
        
    Instruction(
        0x53, "LD D,E", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.D, 1), Operand.reg(Registers.E, 1) ),
        executor = Load),
        
    Instruction(
        0x54, "LD D,H", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.D, 1), Operand.reg(Registers.H, 1) ),
        executor = Load),
        
    Instruction(
        0x55, "LD D,L", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.D, 1), Operand.reg(Registers.L, 1) ),
        executor = Load),
        
    Instruction(
        0x56, "LD D,(HL)", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.D, 1), Operand.regi(Registers.HL, 2) ),
        executor = Load),
        
    Instruction(
        0x57, "LD D,A", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.D, 1), Operand.reg(Registers.A, 1) ),
        executor = Load),
        
    Instruction(
        0x58, "LD E,B", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.E, 1), Operand.reg(Registers.B, 1) ),
        executor = Load),
        
    Instruction(
        0x59, "LD E,C", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.E, 1), Operand.reg(Registers.C, 1) ),
        executor = Load),
        
    Instruction(
        0x5A, "LD E,D", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.E, 1), Operand.reg(Registers.D, 1) ),
        executor = Load),
        
    Instruction(
        0x5B, "LD E,E", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.E, 1), Operand.reg(Registers.E, 1) ),
        executor = Load),
        
    Instruction(
        0x5C, "LD E,H", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.E, 1), Operand.reg(Registers.H, 1) ),
        executor = Load),
        
    Instruction(
        0x5D, "LD E,L", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.E, 1), Operand.reg(Registers.L, 1) ),
        executor = Load),
        
    Instruction(
        0x5E, "LD E,(HL)", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.E, 1), Operand.regi(Registers.HL, 2) ),
        executor = Load),
        
    Instruction(
        0x5F, "LD E,A", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.E, 1), Operand.reg(Registers.A, 1) ),
        executor = Load),
        
    Instruction(
        0x60, "LD H,B", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.H, 1), Operand.reg(Registers.B, 1) ),
        executor = Load),
        
    Instruction(
        0x61, "LD H,C", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.H, 1), Operand.reg(Registers.C, 1) ),
        executor = Load),
        
    Instruction(
        0x62, "LD H,D", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.H, 1), Operand.reg(Registers.D, 1) ),
        executor = Load),
        
    Instruction(
        0x63, "LD H,E", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.H, 1), Operand.reg(Registers.E, 1) ),
        executor = Load),
        
    Instruction(
        0x64, "LD H,H", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.H, 1), Operand.reg(Registers.H, 1) ),
        executor = Load),
        
    Instruction(
        0x65, "LD H,L", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.H, 1), Operand.reg(Registers.L, 1) ),
        executor = Load),
        
    Instruction(
        0x66, "LD H,(HL)", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.H, 1), Operand.regi(Registers.HL, 2) ),
        executor = Load),
        
    Instruction(
        0x67, "LD H,A", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.H, 1), Operand.reg(Registers.A, 1) ),
        executor = Load),
        
    Instruction(
        0x68, "LD L,B", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.L, 1), Operand.reg(Registers.B, 1) ),
        executor = Load),
        
    Instruction(
        0x69, "LD L,C", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.L, 1), Operand.reg(Registers.C, 1) ),
        executor = Load),
        
    Instruction(
        0x6A, "LD L,D", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.L, 1), Operand.reg(Registers.D, 1) ),
        executor = Load),
        
    Instruction(
        0x6B, "LD L,E", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.L, 1), Operand.reg(Registers.E, 1) ),
        executor = Load),
        
    Instruction(
        0x6C, "LD L,H", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.L, 1), Operand.reg(Registers.H, 1) ),
        executor = Load),
        
    Instruction(
        0x6D, "LD L,L", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.L, 1), Operand.reg(Registers.L, 1) ),
        executor = Load),
        
    Instruction(
        0x6E, "LD L,(HL)", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.L, 1), Operand.regi(Registers.HL, 2) ),
        executor = Load),
        
    Instruction(
        0x6F, "LD L,A", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.L, 1), Operand.reg(Registers.A, 1) ),
        executor = Load),
        
    Instruction(
        0x70, "LD (HL),B", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.regi(Registers.HL, 2), Operand.reg(Registers.B, 1) ),
        executor = Load),
        
    Instruction(
        0x71, "LD (HL),C", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.regi(Registers.HL, 2), Operand.reg(Registers.C, 1) ),
        executor = Load),
        
    Instruction(
        0x72, "LD (HL),D", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.regi(Registers.HL, 2), Operand.reg(Registers.D, 1) ),
        executor = Load),
        
    Instruction(
        0x73, "LD (HL),E", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.regi(Registers.HL, 2), Operand.reg(Registers.E, 1) ),
        executor = Load),
        
    Instruction(
        0x74, "LD (HL),H", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.regi(Registers.HL, 2), Operand.reg(Registers.H, 1) ),
        executor = Load),
        
    Instruction(
        0x75, "LD (HL),L", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.regi(Registers.HL, 2), Operand.reg(Registers.L, 1) ),
        executor = Load),
        
    Instruction(
        0x76, "HALT", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = None,
        executor = Halt),
        
    Instruction(
        0x77, "LD (HL),A", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.regi(Registers.HL, 2), Operand.reg(Registers.A, 1) ),
        executor = Load),
        
    Instruction(
        0x78, "LD A,B", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.B, 1) ),
        executor = Load),
        
    Instruction(
        0x79, "LD A,C", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.C, 1) ),
        executor = Load),
        
    Instruction(
        0x7A, "LD A,D", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.D, 1) ),
        executor = Load),
        
    Instruction(
        0x7B, "LD A,E", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.E, 1) ),
        executor = Load),
        
    Instruction(
        0x7C, "LD A,H", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.H, 1) ),
        executor = Load),
        
    Instruction(
        0x7D, "LD A,L", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.L, 1) ),
        executor = Load),
        
    Instruction(
        0x7E, "LD A,(HL)", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.regi(Registers.HL, 2) ),
        executor = Load),
        
    Instruction(
        0x7F, "LD A,A", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = Load),
        
    Instruction(
        0x80, "ADD A,B", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.B, 1) ),
        executor = Add),
        
    Instruction(
        0x81, "ADD A,C", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.C, 1) ),
        executor = Add),
        
    Instruction(
        0x82, "ADD A,D", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.D, 1) ),
        executor = Add),
        
    Instruction(
        0x83, "ADD A,E", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.E, 1) ),
        executor = Add),
        
    Instruction(
        0x84, "ADD A,H", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.H, 1) ),
        executor = Add),
        
    Instruction(
        0x85, "ADD A,L", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.L, 1) ),
        executor = Add),
        
    Instruction(
        0x86, "ADD A,(HL)", bus_width=1,
        byte_size=1, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.regi(Registers.HL, 2) ),
        executor = Add),
        
    Instruction(
        0x87, "ADD A,A", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = Add),
        
    Instruction(
        0x88, "ADC A,B", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.B, 1) ),
        executor = AddWithCarry),
        
    Instruction(
        0x89, "ADC A,C", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.C, 1) ),
        executor = AddWithCarry),
        
    Instruction(
        0x8A, "ADC A,D", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.D, 1) ),
        executor = AddWithCarry),
        
    Instruction(
        0x8B, "ADC A,E", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.E, 1) ),
        executor = AddWithCarry),
        
    Instruction(
        0x8C, "ADC A,H", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.H, 1) ),
        executor = AddWithCarry),
        
    Instruction(
        0x8D, "ADC A,L", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.L, 1) ),
        executor = AddWithCarry),
        
    Instruction(
        0x8E, "ADC A,(HL)", bus_width=1,
        byte_size=1, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.regi(Registers.HL, 2) ),
        executor = AddWithCarry),
        
    Instruction(
        0x8F, "ADC A,A", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = AddWithCarry),
        
    Instruction(
        0x90, "SUB B", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.B, 1) ),
        executor = Subtract),
        
    Instruction(
        0x91, "SUB C", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.C, 1) ),
        executor = Subtract),
        
    Instruction(
        0x92, "SUB D", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.D, 1) ),
        executor = Subtract),
        
    Instruction(
        0x93, "SUB E", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.E, 1) ),
        executor = Subtract),
        
    Instruction(
        0x94, "SUB H", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.H, 1) ),
        executor = Subtract),
        
    Instruction(
        0x95, "SUB L", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.L, 1) ),
        executor = Subtract),
        
    Instruction(
        0x96, "SUB (HL)", bus_width=1,
        byte_size=1, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.regi(Registers.HL, 2) ),
        executor = Subtract),
        
    Instruction(
        0x97, "SUB A", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = Subtract),
        
    Instruction(
        0x98, "SBC A,B", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.B, 1) ),
        executor = SubWithCarry),
        
    Instruction(
        0x99, "SBC A,C", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.C, 1) ),
        executor = SubWithCarry),
        
    Instruction(
        0x9A, "SBC A,D", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.D, 1) ),
        executor = SubWithCarry),
        
    Instruction(
        0x9B, "SBC A,E", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.E, 1) ),
        executor = SubWithCarry),
        
    Instruction(
        0x9C, "SBC A,H", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.H, 1) ),
        executor = SubWithCarry),
        
    Instruction(
        0x9D, "SBC A,L", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.L, 1) ),
        executor = SubWithCarry),
        
    Instruction(
        0x9E, "SBC A,(HL)", bus_width=1,
        byte_size=1, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.regi(Registers.HL, 2) ),
        executor = SubWithCarry),
        
    Instruction(
        0x9F, "SBC A,A", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = SubWithCarry),
        
    Instruction(
        0xA0, "AND B", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.B, 1) ),
        executor = BinAnd),
        
    Instruction(
        0xA1, "AND C", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.C, 1) ),
        executor = BinAnd),
        
    Instruction(
        0xA2, "AND D", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.D, 1) ),
        executor = BinAnd),
        
    Instruction(
        0xA3, "AND E", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.E, 1) ),
        executor = BinAnd),
        
    Instruction(
        0xA4, "AND H", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.H, 1) ),
        executor = BinAnd),
        
    Instruction(
        0xA5, "AND L", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.L, 1) ),
        executor = BinAnd),
        
    Instruction(
        0xA6, "AND (HL)", bus_width=1,
        byte_size=1, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.regi(Registers.HL, 2) ),
        executor = BinAnd),
        
    Instruction(
        0xA7, "AND A", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = BinAnd),
        
    Instruction(
        0xA8, "XOR B", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.B, 1) ),
        executor = BinXor),
        
    Instruction(
        0xA9, "XOR C", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.C, 1) ),
        executor = BinXor),
        
    Instruction(
        0xAA, "XOR D", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.D, 1) ),
        executor = BinXor),
        
    Instruction(
        0xAB, "XOR E", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.E, 1) ),
        executor = BinXor),
        
    Instruction(
        0xAC, "XOR H", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.H, 1) ),
        executor = BinXor),
        
    Instruction(
        0xAD, "XOR L", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.L, 1) ),
        executor = BinXor),
        
    Instruction(
        0xAE, "XOR (HL)", bus_width=1,
        byte_size=1, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.regi(Registers.HL, 2) ),
        executor = BinXor),
        
    Instruction(
        0xAF, "XOR A", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = BinXor),
        
    Instruction(
        0xB0, "OR B", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.B, 1) ),
        executor = BinOr),
        
    Instruction(
        0xB1, "OR C", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.C, 1) ),
        executor = BinOr),
        
    Instruction(
        0xB2, "OR D", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.D, 1) ),
        executor = BinOr),
        
    Instruction(
        0xB3, "OR E", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.E, 1) ),
        executor = BinOr),
        
    Instruction(
        0xB4, "OR H", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.H, 1) ),
        executor = BinOr),
        
    Instruction(
        0xB5, "OR L", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.L, 1) ),
        executor = BinOr),
        
    Instruction(
        0xB6, "OR (HL)", bus_width=1,
        byte_size=1, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.regi(Registers.HL, 2) ),
        executor = BinOr),
        
    Instruction(
        0xB7, "OR A", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.reg(Registers.A, 1) ),
        executor = BinOr),
        
    Instruction(
        0xB8, "CP B", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, throwaway = True), Operand.reg(Registers.B, 1) ),
        executor = Compare),
        
    Instruction(
        0xB9, "CP C", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, throwaway = True), Operand.reg(Registers.C, 1) ),
        executor = Compare),
        
    Instruction(
        0xBA, "CP D", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, throwaway = True), Operand.reg(Registers.D, 1) ),
        executor = Compare),
        
    Instruction(
        0xBB, "CP E", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, throwaway = True), Operand.reg(Registers.E, 1) ),
        executor = Compare),
        
    Instruction(
        0xBC, "CP H", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, throwaway = True), Operand.reg(Registers.H, 1) ),
        executor = Compare),
        
    Instruction(
        0xBD, "CP L", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, throwaway = True), Operand.reg(Registers.L, 1) ),
        executor = Compare),
        
    Instruction(
        0xBE, "CP (HL)", bus_width=1,
        byte_size=1, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, throwaway = True), Operand.regi(Registers.HL, 2) ),
        executor = Compare),
        
    Instruction(
        0xBF, "CP A", bus_width=1,
        byte_size=1, cycles=4,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, throwaway = True), Operand.reg(Registers.A, 1) ),
        executor = Compare),
        
    Instruction(
        0xC0, "RET NZ", bus_width=1,
        byte_size=1, cycles=20/8,
        flags=None,
        operands = ( None, Operand.bit(Flag.z, Bit.Reset) ),
        executor = Return),
        
    Instruction(
        0xC1, "POP BC", bus_width=2,
        byte_size=1, cycles=12,
        flags=None,
        operands = ( Operand.reg(Registers.BC, 2), Operand.reg(Registers.BC, 2) ),
        executor = Pop),
        
    Instruction(
        0xC2, "JP NZ,a16", bus_width=1,
        byte_size=3, cycles=16/12,
        flags=None,
        operands = ( Operand.bit(Flag.z, Bit.Reset), Operand.imm(2) ),
        executor = Jump),
        
    Instruction(
        0xC3, "JP a16", bus_width=1,
        byte_size=3, cycles=16,
        flags=None,
        operands = ( None, Operand.imm(2) ),
        executor = Jump),
        
    Instruction(
        0xC4, "CALL NZ,a16", bus_width=1,
        byte_size=3, cycles=24/12,
        flags=None,
        operands = ( Operand.bit(Flag.z, Bit.Reset), Operand.imm(2) ),
        executor = Call),
        
    Instruction(
        0xC5, "PUSH BC", bus_width=2,
        byte_size=1, cycles=16,
        flags=None,
        operands = ( None, Operand.reg(Registers.BC, 2) ),
        executor = Push),
        
    Instruction(
        0xC6, "ADD A,d8", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.imm(1) ),
        executor = Add),
        
    Instruction(
        0xC7, "RST 00H", bus_width=1,
        byte_size=1, cycles=16,
        flags=None,
        operands = ( None, Operand.const(0x00) ),
        executor = Restart),
        
    Instruction(
        0xC8, "RET Z", bus_width=1,
        byte_size=1, cycles=20/8,
        flags=None,
        operands = ( None, Operand.bit(Flag.z, Bit.Set) ),
        executor = Return),
        
    Instruction(
        0xC9, "RET", bus_width=1,
        byte_size=1, cycles=16,
        flags=None,
        operands = None,
        executor = Return),
        
    Instruction(
        0xCA, "JP Z,a16", bus_width=1,
        byte_size=3, cycles=16/12,
        flags=None,
        operands = ( Operand.bit(Flag.z, Bit.Set), Operand.imm(2) ),
        executor = Jump),
        
    Instruction(
        0xCB, "PREFIX CB", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = None,
        executor = InvalidInstruction),
        
    Instruction(
        0xCC, "CALL Z,a16", bus_width=1,
        byte_size=3, cycles=24/12,
        flags=None,
        operands = ( Operand.bit(Flag.z, Bit.Set), Operand.imm(2) ),
        executor = Call),
        
    Instruction(
        0xCD, "CALL a16", bus_width=1,
        byte_size=3, cycles=24,
        flags=None,
        operands = ( None, Operand.imm(2) ),
        executor = Call),
        
    Instruction(
        0xCE, "ADC A,d8", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.imm(1) ),
        executor = AddWithCarry),
        
    Instruction(
        0xCF, "RST 08H", bus_width=1,
        byte_size=1, cycles=16,
        flags=None,
        operands = ( None, Operand.const(0x08) ),
        executor = Restart),
        
    Instruction(
        0xD0, "RET NC", bus_width=1,
        byte_size=1, cycles=20/8,
        flags=None,
        operands = ( None, Operand.bit(Flag.c, Bit.Reset) ),
        executor = Return),
        
    Instruction(
        0xD1, "POP DE", bus_width=2,
        byte_size=1, cycles=12,
        flags=None,
        operands = ( Operand.reg(Registers.DE, 2), Operand.reg(Registers.DE, 2) ),
        executor = Pop),
        
    Instruction(
        0xD2, "JP NC,a16", bus_width=1,
        byte_size=3, cycles=16/12,
        flags=None,
        operands = ( Operand.bit(Flag.c, Bit.Reset), Operand.imm(2) ),
        executor = Jump),
        
    Instruction(
        0xD3, "INVALID", bus_width=1,
        byte_size=-1, cycles=-1,
        flags=None,
        operands = None,
        executor = InvalidInstruction),
        
    Instruction(
        0xD4, "CALL NC,a16", bus_width=1,
        byte_size=3, cycles=24/12,
        flags=None,
        operands = ( Operand.bit(Flag.c, Bit.Reset), Operand.imm(2) ),
        executor = Call),
        
    Instruction(
        0xD5, "PUSH DE", bus_width=2,
        byte_size=1, cycles=16,
        flags=None,
        operands = ( None, Operand.reg(Registers.DE, 2) ),
        executor = Push),
        
    Instruction(
        0xD6, "SUB d8", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.imm(1) ),
        executor = Subtract),
        
    Instruction(
        0xD7, "RST 10H", bus_width=1,
        byte_size=1, cycles=16,
        flags=None,
        operands = ( None, Operand.const(0x10) ),
        executor = Restart),
        
    Instruction(
        0xD8, "RET C", bus_width=1,
        byte_size=1, cycles=20/8,
        flags=None,
        operands = ( None, Operand.reg(Registers.C, 1) ),
        executor = Return),
        
    Instruction(
        0xD9, "RETI", bus_width=1,
        byte_size=1, cycles=16,
        flags=None,
        operands = None,
        executor = ReturnInterrupt),
        
    Instruction(
        0xDA, "JP C,a16", bus_width=1,
        byte_size=3, cycles=16/12,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.imm(2) ),
        executor = Jump),
        
    Instruction(
        0xDB, "INVALID", bus_width=1,
        byte_size=-1, cycles=-1,
        flags=None,
        operands = None,
        executor = InvalidInstruction),
        
    Instruction(
        0xDC, "CALL C,a16", bus_width=1,
        byte_size=3, cycles=24/12,
        flags=None,
        operands = ( Operand.reg(Registers.C, 1), Operand.imm(2) ),
        executor = Call),
        
    Instruction(
        0xDD, "INVALID", bus_width=1,
        byte_size=-1, cycles=-1,
        flags=None,
        operands = None,
        executor = InvalidInstruction),
        
    Instruction(
        0xDE, "SBC A,d8", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, 1), Operand.imm(1) ),
        executor = SubWithCarry),
        
    Instruction(
        0xDF, "RST 18H", bus_width=1,
        byte_size=1, cycles=16,
        flags=None,
        operands = ( None, Operand.const(0x18) ),
        executor = Restart),
        
    Instruction(
        0xE0, "LDH (a8),A", bus_width=1,
        byte_size=2, cycles=12,
        flags=None,
        operands = ( Operand.mem(1), Operand.reg(Registers.A, 1) ),
        executor = Load),
        
    Instruction(
        0xE1, "POP HL", bus_width=2,
        byte_size=1, cycles=12,
        flags=None,
        operands = ( Operand.reg(Registers.HL, 2), Operand.reg(Registers.HL, 2) ),
        executor = Pop),
        
    Instruction(
        0xE2, "LD (C),A", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.regi(Registers.C, 1), Operand.reg(Registers.A, 1) ),
        executor = Load),
        
    Instruction(
        0xE3, "INVALID", bus_width=1,
        byte_size=-1, cycles=-1,
        flags=None,
        operands = None,
        executor = InvalidInstruction),
        
    Instruction(
        0xE4, "INVALID", bus_width=1,
        byte_size=-1, cycles=-1,
        flags=None,
        operands = None,
        executor = InvalidInstruction),
        
    Instruction(
        0xE5, "PUSH HL", bus_width=2,
        byte_size=1, cycles=16,
        flags=None,
        operands = ( None, Operand.reg(Registers.HL, 2) ),
        executor = Push),
        
    Instruction(
        0xE6, "AND d8", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Set, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.imm(1) ),
        executor = BinAnd),
        
    Instruction(
        0xE7, "RST 20H", bus_width=1,
        byte_size=1, cycles=16,
        flags=None,
        operands = ( None, Operand.const(0x20) ),
        executor = Restart),
        
    Instruction(
        0xE8, "ADD SP,r8", bus_width=2,
        byte_size=2, cycles=16,
        flags={ Flag.z:Bit.Reset, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.SP, 2), Operand.imm(1) ),
        executor = Add),
        
    Instruction(
        0xE9, "JP (HL)", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = ( None, Operand.regi(Registers.HL, 2) ),
        executor = Jump),
        
    Instruction(
        0xEA, "LD (a16),A", bus_width=1,
        byte_size=3, cycles=16,
        flags=None,
        operands = ( Operand.mem(2), Operand.reg(Registers.A, 1) ),
        executor = Load),
        
    Instruction(
        0xEB, "INVALID", bus_width=1,
        byte_size=-1, cycles=-1,
        flags=None,
        operands = None,
        executor = InvalidInstruction),
        
    Instruction(
        0xEC, "INVALID", bus_width=1,
        byte_size=-1, cycles=-1,
        flags=None,
        operands = None,
        executor = InvalidInstruction),
        
    Instruction(
        0xED, "INVALID", bus_width=1,
        byte_size=-1, cycles=-1,
        flags=None,
        operands = None,
        executor = InvalidInstruction),
        
    Instruction(
        0xEE, "XOR d8", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.imm(1) ),
        executor = BinXor),
        
    Instruction(
        0xEF, "RST 28H", bus_width=1,
        byte_size=1, cycles=16,
        flags=None,
        operands = ( None, Operand.const(0x28) ),
        executor = Restart),
        
    Instruction(
        0xF0, "LDH A,(a8)", bus_width=1,
        byte_size=2, cycles=12,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.mem(1) ),
        executor = Load),
        
    Instruction(
        0xF1, "POP AF", bus_width=2,
        byte_size=1, cycles=12,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Calculate, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.AF, 2), Operand.reg(Registers.AF, 2) ),
        executor = Pop),
        
    Instruction(
        0xF2, "LD A,(C)", bus_width=1,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.regi(Registers.C, 1) ),
        executor = Load),
        
    Instruction(
        0xF3, "DI", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = None,
        executor = DisableInterrupts),
        
    Instruction(
        0xF4, "INVALID", bus_width=1,
        byte_size=-1, cycles=-1,
        flags=None,
        operands = None,
        executor = InvalidInstruction),
        
    Instruction(
        0xF5, "PUSH AF", bus_width=2,
        byte_size=1, cycles=16,
        flags=None,
        operands = ( None, Operand.reg(Registers.AF, 2) ),
        executor = Push),
        
    Instruction(
        0xF6, "OR d8", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Reset, Flag.h:Bit.Reset, Flag.c:Bit.Reset },
        operands = ( Operand.reg(Registers.A, 1), Operand.imm(1) ),
        executor = BinOr),
        
    Instruction(
        0xF7, "RST 30H", bus_width=1,
        byte_size=1, cycles=16,
        flags=None,
        operands = ( None, Operand.const(0x30) ),
        executor = Restart),
        
    Instruction(
        0xF8, "LD HL,SP+r8", bus_width=2,
        byte_size=2, cycles=12,
        flags={ Flag.z:Bit.Reset, Flag.n:Bit.Reset, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.HL, 2), Operand.regI(Registers.SP) ),
        executor = Load),
        
    Instruction(
        0xF9, "LD SP,HL", bus_width=2,
        byte_size=1, cycles=8,
        flags=None,
        operands = ( Operand.reg(Registers.SP, 2), Operand.reg(Registers.HL, 2) ),
        executor = Load),
        
    Instruction(
        0xFA, "LD A,(a16)", bus_width=1,
        byte_size=3, cycles=16,
        flags=None,
        operands = ( Operand.reg(Registers.A, 1), Operand.mem(2) ),
        executor = Load),
        
    Instruction(
        0xFB, "EI", bus_width=1,
        byte_size=1, cycles=4,
        flags=None,
        operands = None,
        executor = EnableInterrupts),
        
    Instruction(
        0xFC, "INVALID", bus_width=1,
        byte_size=-1, cycles=-1,
        flags=None,
        operands = None,
        executor = InvalidInstruction),
        
    Instruction(
        0xFD, "INVALID", bus_width=1,
        byte_size=-1, cycles=-1,
        flags=None,
        operands = None,
        executor = InvalidInstruction),
        
    Instruction(
        0xFE, "CP d8", bus_width=1,
        byte_size=2, cycles=8,
        flags={ Flag.z:Bit.Calculate, Flag.n:Bit.Set, Flag.h:Bit.Calculate, Flag.c:Bit.Calculate },
        operands = ( Operand.reg(Registers.A, throwaway = True), Operand.imm(1) ),
        executor = Compare),
        
    Instruction(
        0xFF, "RST 38H", bus_width=1,
        byte_size=1, cycles=16,
        flags=None,
        operands = ( None, Operand.const(0x38) ),
        executor = Restart),
        
]

