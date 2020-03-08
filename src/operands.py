from enum import Enum
from .cpu_types import *

class Addressing(Enum):
    """Enum for establishing the instruction operand Addressing mode"""
    # Operand is a constant value (which is *not* immediate)
    Constant = 'c'

    # Operand is CPU bit value
    Bit = 'b'

    # Operand value is in the instruction
    Immediate = 'I'

    # Uses a CPU register as value
    Register = 'R'

    # Uses indirect value and does R+1
    RegisterIncrement = 'R+'
    # Uses indirect value and does R-1
    RegisterDecrement = 'R-'

    # Uses the Register + what is given by the operand
    RegisterPlusImmediate = 'RI'

    # Uses the register as an indirection for the value
    RegisterIndirect = 'Ri'

    # Operand location is in the instruction
    # Value is obtained by dereferencing
    Direct = 'D'

    # Operand pointer is at location
    Indirect = 'i'
#end bits

class BaseOperand:
    def __init__(self, width, addressing_mode):
        # Always used
        self._mode = addressing_mode
        self.width = width # 1 or 2 bytes
        self._throwaway = False
    #end

    def get_value(self, cpu, mem, location):
        "Gets the value of the operand"
        raise NotImplementedError()
    def set_value(self, cpu, mem, location, value):
        "Sets the value of the operand. Use for writeback step"
        raise NotImplementedError()
    #end

    def _translate_address(self, address):
        if self.width == 1:
            if type(address) is bytearray:
                address = address[0]
            address = address | 0xFF00
        return address

    def can_set_value(self):
        """Checks if this operand can be used to set value"""
        return self._mode != Addressing.Immediate and self._mode != Addressing.RegisterPlusImmediate \
            and self._mode != Addressing.Bit and self._mode != Addressing.Constant
    #end

    def ToString(self, mem, address):
        """
        Returns a string that can be better read alongside similar strings for reading
        """
        # Returns something like "A", "(BC)", "imm"
        if self._mode != Addressing.Direct and self._mode != Addressing.Immediate:
            return self.__str__()

        formatter = "0x{0:02X}" if self.width == 1 else "0x{0:04X}"
        val = int.from_bytes(mem.Read(address, self.width), 'little')
        base = formatter.format(val)
        return base if self._mode == Addressing.Immediate else ("({})".format(base))
    #end

    def __eq__(self, other):
        # Two operands are equal if they are operating on registers with the same mode and have the same width
        # We can't say memory operands are equal without binding to the address
        return self._mode == other._mode and\
             (self._mode != Addressing.Immediate and self._mode != Addressing.Direct)\
                  and self.width == other.width and self._register == other._register

    def __str__(self):
        """
        String that describes the operand.
        Returns something like "A", "(BC)", "imm"
        """
        if self._mode == Addressing.Immediate:
            return "imm"
        elif self._mode == Addressing.Register:
            return GetRegisterName(self._register, self.width)
        elif self._mode == Addressing.RegisterIndirect:
            return "(%s)" % GetRegisterName(self._register, self.width)
        elif self._mode == Addressing.RegisterDecrement or self._mode == Addressing.RegisterIncrement:
            symbol = '+' if self._mode == Addressing.RegisterIncrement else '-'
            return "({}{})".format(GetRegisterName(self._register, self.width), symbol)
        elif self._mode == Addressing.Direct:
            return "(addr)"
        elif self._mode == Addressing.Constant:
            return "{:X}H".format(self._value) if self._value > 7 else str(self._value)
        elif self._mode == Addressing.Bit:
            name = self._bit.name.upper()
            return name if self._bit_state == Bit.Set else "N"+name

        return "Unsupported addressing mode operand"
    #end

    def __repr__(self):
        """
        Debugging representation of the operand
        Returns something like
        "<Operand '(HL)' at 0x7f0ff7d6b100>"
        """
        return "<Operand '{0}' at {1}>".format(
            str(self),
            hex(id(self))
        )
    #end
#end BaseOperand

class ConstOperand(BaseOperand):
    def __init__(self, value):
        super().__init__(1, Addressing.Constant)
        self._value = value
    def get_value(self, cpu, mem, location):
        "Gets the value of the operand"
        return self._value
    def set_value(self, cpu, mem, location, value):
        raise ValueError("A constant-value operand cannot be written to!")
    #end
#end class

class BitOperand(BaseOperand):
    def __init__(self, offset, state):
        super().__init__(1, Addressing.Bit)
        self._bit = offset
        self._expected = state
    def get_value(self, cpu, mem, location):
        "Gets the value of the operand"
        a_bit = cpu.get_flag(self._bit)
        return a_bit if self._expected == Bit.Set else (not a_bit)
    def set_value(self, cpu, mem, location, value):
        raise ValueError("A bit operand should not be written to directly!")
    #end
#end class

class ImmediateOperand(BaseOperand):
    def __init__(self, width):
        super().__init__(width, Addressing.Immediate)
    #end

    def _to_num(self, value):
        if self.width == 1:
            return value[0]

        # TODO: Optimize based on this
        assert(self.width == 2)
        return int.from_bytes(value, 'little')
    def get_value(self, cpu, mem, location):
        "Gets the value of the operand"
        return self._to_num(mem.Read(location, self.width))
    def set_value(self, cpu, mem, location, value):
        raise ValueError("An immediate mode operand cannot be written to!")
    #end
#end class

class DirectOperand(ImmediateOperand):
    def __init__(self, width):
        super().__init__(width, Addressing.Direct)

    def get_value(self, cpu, mem, location):
        "Gets the value of the operand"
        return mem.Read(self._translate_address(super.get_value()), self.width)
    def set_value(self, cpu, mem, location, value):
        address = mem.Read(location, self.width)
        mem.Write(self._translate_address(address), value)
    #end
#end class

class RegisterOperand(BaseOperand):
    def __init__(self, reg, width, mode = Addressing.Register):
        super().__init__(width, mode)
        self._register = reg
    #end

    def _to_bytes(self, value):
        wb_v = value
        if type(wb_v) is int:
            num_bytes = 1 if self._register != Registers.SP else 2
            wb_v = value.to_bytes(num_bytes, 'little')
        return wb_v
    def _get_register(self, cpu):
        if self._register < 0:
            return cpu.SP if self._register == Registers.SP else cpu.PC
        return cpu.get_register(self._register, self.width)
    def _set_register(self, cpu, new_value):
        if self._register < 0:
            if self._register == Registers.SP:
                cpu.SP = new_value
            else:
                cpu.PC = new_value
        else:
            cpu.set_register(new_value, self._register, self.width)
    #end

    def get_value(self, cpu, mem, location):
        "Gets the value of the operand"
        return self._get_register(cpu)
    def set_value(self, cpu, mem, location, value):
        "Sets the value of the operand. Use for writeback step"
        self._set_register(cpu, value)
    #end
#end class

class RegisterIndirectOperand(RegisterOperand):
    def __init__(self, reg, width):
        RegisterOperand.__init__(self, reg, width, Addressing.RegisterIndirect)
        self._register = reg
    #end

    def get_value(self, cpu, mem, location):
        "Gets the value of the operand"
        # Reads 1 byte of data
        return mem.Read(self._translate_address(self._get_register(cpu)), self.width)[0]
    def set_value(self, cpu, mem, location, value):
        "Sets the value of the operand. Use for writeback step"
        # writes 1 byte of data
        mem.Write(self._translate_address(self._get_register(cpu)), bytes([value]))
    #end
#end class

class RegisterPostOperand(RegisterOperand):
    def __init__(self, reg, width, mode):
        RegisterOperand.__init__(self, reg, width, mode)
        self._register = reg

        inc = lambda x: x+1
        dec = lambda x: x-1
        self._postop = inc if self._mode == Addressing.RegisterIncrement else dec
        self._old_val = None
    #end

    def _do_postop(self, cpu):
        #Set the new value immediately
        value = self._get_register(cpu)
        new_value = self._postop(value)
        self._set_register(cpu, new_value)
        self._old_val = value
    #end

    def get_value(self, cpu, mem, location):
        "Gets the value of the operand"
        value = self._get_register(cpu)
        self._do_postop(cpu)
        return mem.Read(self._translate_address(value))[0]
    def set_value(self, cpu, mem, location, value):
        "Sets the value of the operand. Use for writeback step"
        assert(self._old_val is not None)
        mem.Write(self._translate_address(self._old_val), bytes([value]))
        self._old_val = None
    #end
#end

class RegisterAndImmediateOperand(RegisterOperand):
    def __init__(self, reg):
        super().__init__(reg, 2, Addressing.RegisterPlusImmediate)
        self._register = reg
    #end

    def get_value(self, cpu, mem, location):
        "Gets the value of the operand"
        # Reads 1 byte of data
        return super.get_value(cpu, mem, location) + (mem.Read(location)[0])
    def set_value(self, cpu, mem, location, value):
        raise ValueError("An immediate mode operand cannot be written to!")
    #end
#end class

class Operand(BaseOperand):
    """
    Internal representation of an instruction operand
    This is used both for binding (get/set) and debugging purposes
    """

    def __init__(self, reg, width, addressing_mode):
        # Always used
        self._mode = addressing_mode
        self.width = width # 1 or 2 bytes

        # used when operands constants, bits, register enums
        self._register = reg
        self._throwaway = False

        # only used when bits are used to determine if we're checking set or reset bits
        # which is why we provide a default value
        self._bit_state = Bit.Ignore
    #end

    @staticmethod
    def bit(offset, state):
        op = BitOperand(offset, state)
        op._bit_state = state
        return op

    @staticmethod
    def const(value):
        return ConstOperand(value)

    @staticmethod
    def reg(reg, width=1, throwaway = False):
        op = RegisterOperand(reg, width)
        return op

    @staticmethod
    def regi(reg, width=1):
        return RegisterIndirectOperand(reg, width)

    @staticmethod
    def regI(reg):
        return RegisterAndImmediateOperand(reg)

    @staticmethod
    def regInc(reg, width=1):
        return RegisterPostOperand(reg, width, Addressing.RegisterIncrement)

    @staticmethod
    def regDec(reg, width=1):
        return RegisterPostOperand(reg, width, Addressing.RegisterDecrement)

    @staticmethod
    def imm(width):
        return ImmediateOperand(width)

    @staticmethod
    def mem(width):
        return Operand(None, width, Addressing.Direct)

    def can_set_value(self):
        """Checks if this operand can be used to set value"""
        return self._mode != Addressing.Immediate and self._mode != Addressing.RegisterPlusImmediate \
            and self._mode != Addressing.Bit and self._mode != Addressing.Constant

    def _get_register(self, cpu):
        if self._register < 0:
            return cpu.SP if self._register == Registers.SP else cpu.PC
        return cpu.get_register(self._register, self.width)

    def _translate_address(self, address):
        if self.width == 1:
            if type(address) is bytearray:
                address = address[0]
            address = address | 0xFF00
        return address

    def _postop(self, cpu):
        #Set the new value immediately
        value = self._get_register(cpu)
        new_value = value + 1 if self._mode == Addressing.RegisterIncrement else value - 1

        if self._register < 0:
            if self._register == Registers.SP:
                cpu.SP = new_value
            else:
                cpu.PC = new_value
        else:
            cpu.set_register(new_value, self._register, self.width)
        #end if-else
    #end

    def _previous_value(self, cpu):
        # Get the previously used value
        value = self._get_register(cpu)
        return value - 1 if self._mode == Addressing.RegisterIncrement else value + 1

    def get_value(self, cpu, mem, location):
        "Gets the value of the operand"

        # if we're retrieving a constant, just return immediately
        if self._mode == Addressing.Constant:
            return self._register

        # Methods that will get the value
        def bit():
            a_bit = cpu.get_flag(self._register)
            return a_bit if self._bit_state == Bit.Set else (not a_bit)
        def immediate():
            return mem.Read(location, self.width)
        def register():
            return self._get_register(cpu)
        def register_post():
            value = register()
            self._postop(cpu)
            return mem.Read(self._translate_address(value))
        def register_w_immediate():
            return register() + immediate()
        def reg_indirect():
            return mem.Read(self._translate_address(register()), self.width)
        def direct():
            return mem.Read(self._translate_address(immediate()), self.width)
        def indirect():
            return mem.Read(self._translate_address(direct()), self.width)

        value_map = {
            Addressing.Bit: bit,
            Addressing.Immediate: immediate,
            Addressing.Register: register,
            Addressing.RegisterIncrement: register_post,
            Addressing.RegisterDecrement: register_post,
            Addressing.RegisterPlusImmediate: register_w_immediate,
            Addressing.RegisterIndirect: reg_indirect,
            Addressing.Direct: direct,
            Addressing.Indirect: indirect
        }

        retVal = value_map[self._mode]()
        if type(retVal) is bytearray:
            retVal = int.from_bytes(retVal, 'little')
        return retVal
    #end get_value

    def set_value(self, cpu, mem, location, value):
        "Sets the value of the operand. Use for writeback step"

        # Throw exception now so we know
        if self._mode == Addressing.Immediate or self._mode == Addressing.RegisterPlusImmediate:
            raise ValueError("An immediate mode operand cannot be written to!")
        elif self._mode == Addressing.Constant:
            raise ValueError("A constant-value operand cannot be written to!")
        elif self._mode == Addressing.Bit:
            raise ValueError("A bit operand should not be written to directly!")

        def safe_val():
            wb_v = value
            if type(wb_v) is int:
                num_bytes = 1 if self._register != Registers.SP else 2
                wb_v = value.to_bytes(num_bytes, 'little')
            return wb_v

        # Methods that will get the value
        def register():
            if self._register < 0:
                if self._register == Registers.SP:
                    cpu.SP = value
                else:
                    cpu.PC = value
            else:
                cpu.set_register(value, self._register, self.width)
        def reg_indirect():
            mem.Write(self._translate_address(self._get_register(cpu)), safe_val())
        def register_post():
            mem.Write(self._translate_address(self._previous_value(cpu)), safe_val())
        def direct():
            address = mem.Read(location, self.width)
            mem.Write(self._translate_address(address), value)
        def indirect():
            indirect_loc = mem.Read(location, self.width)
            return mem.Read(self._translate_address(indirect_loc), self.width)

        value_map = {
            Addressing.Register: register,
            Addressing.RegisterIncrement: register_post,
            Addressing.RegisterDecrement: register_post,
            Addressing.RegisterIndirect: reg_indirect,
            Addressing.Direct: direct,
            Addressing.Indirect: indirect
        }

        value_map[self._mode]()
    #end set_value
#end operand