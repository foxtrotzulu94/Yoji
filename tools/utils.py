class TextInstruction:
    from json import JSONEncoder
    class Serializer(JSONEncoder):
        def default(self, o):
            return o.__dict__

    def __init__(self, opcode):
        self.opcode = opcode
        self.mnemonic = "INVALID"
        self.bytes = -1
        self.cycles = -1
        self.flags = None

    def __str__(self):
        return "{} {} {} {}".format(self.mnemonic, self.bytes, self.cycles, self.flags)

    def __repr__(self):
        return self.__str__()