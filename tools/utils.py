class TextInstruction:
    from json import JSONEncoder
    class Serializer(JSONEncoder):
        def default(self, o):
            return o.__dict__

    @staticmethod
    def from_json(data):
        obj = TextInstruction(0)
        obj.__dict__ = data
        return obj

    def __init__(self, opcode):
        self.opcode = opcode
        self.mnemonic = "INVALID"
        self.operands = None
        self.bytes = -1
        self.cycles = -1
        self.flags = None
        self.width = 1

    def __str__(self):
        return "{} {} {} {}".format(self.mnemonic, self.bytes, self.cycles, self.flags)

    def __repr__(self):
        return self.__str__()

def tokenize_mnemonic(instr):
    """
    Returns a list of tokens
    The first token is the operation and all subsequent tokens are operands
    """

    tokens = instr.mnemonic.split()
    base = tokens[0]
    dst = src = None
    if len(tokens) < 2:
        # Only single token (the operation)
        return ( base ,)

    else:
        op_tks = tokens[1]
        if ',' in op_tks:
            dst, src = op_tks.split(',')
            return (base, dst, src)
        else:
            return (base, op_tks)
    #end if-else on tokens

class RefinedInstruction:
    from json import JSONEncoder
    class Serializer(JSONEncoder):
        def default(self, o):
            return o.__dict__

    def __init__(self, txt_instr, prefix = None):
        # do a full copy
        self.__dict__ = txt_instr.__dict__
        self.prefix = prefix
        # BUT override some values and compute others
        tokens = tokenize_mnemonic(txt_instr)
        self.operation = tokens[0]
        self.operands = tokens[1:]
        self.bytes = int(self.bytes)
        self.cycles = int(self.cycles) if type(self.cycles) is int or not '/' in self.cycles else [int(x) for x in self.cycles.split('/')]
        temp_flags = self.flags
        if temp_flags is not None:
            self.flags = None if all(x == '-' for x in temp_flags) else temp_flags
        if self.flags is not None:
            self.flags = dict(zip(['z', 'n', 'h', 'c'], self.flags))

        self.opcode_bin = bin(self.opcode)
        self.opcode_hex = hex(self.opcode)

