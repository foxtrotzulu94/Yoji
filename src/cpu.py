class CPU:
    def __init__(self):
        # registers
        self.__program_counter = 0
        self.__stack_ptr = 0
        self.__registers = bytearray(2 * 4)

    def __get_flag(self, bit_offset):
        return (self.__registers[1] & (1 << bit_offset)) == (1 << bit_offset)

    def __set_flag(self, value, bit_offset):
        if type(value) is int:
            value = True if value > 0 else False

        if value:
            self.__registers[1] = self.__registers[1] | 1 << bit_offset
        else:
            self.__registers[1] = (self.__registers[1] & ~(1 << bit_offset))

    def _generate_get_flag(bit_offset):
        def gen(self):
            return self.__get_flag(bit_offset)
        return gen

    def _generate_set_flag(bit_offset):
        def gen(self, value):
            return self.__set_flag(value, bit_offset)
        return gen

    @property
    def A(self):
        """ Sets the 8-bit Accumulator register """
        return self.__registers[0]

    @A.setter
    def A(self, value):
        if type(value) is int:
            value = bytearray(value.to_bytes(1, 'big'))
        self.__registers[0] = value

    @property
    def F(self):
        """ Sets the Entire Flag register """
        return self.__registers[1]

    @F.setter
    def F(self, value):
        self.__registers[1] = value

    Z = property(_generate_get_flag(7), _generate_set_flag(7), None, "The Zero bit flag")
    N = property(_generate_get_flag(6), _generate_set_flag(6), None, "The Subtract bit flag")
    H = property(_generate_get_flag(5), _generate_set_flag(5), None, "The Half Carry bit flag")
    C = property(_generate_get_flag(4), _generate_set_flag(4), None, "The Carry bit flag")

    @property
    def HL(self):
        """ Sets the 16-bit wide HL register """
        return self.__registers[6:8]

    @HL.setter
    def HL(self, value):
        if type(value) is int:
            value = bytearray(value.to_bytes(2, 'big'))
        self.__registers[6:8] = value