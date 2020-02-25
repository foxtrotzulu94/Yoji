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
        self.bytes = -1
        self.cycles = -1
        self.flags = None
        self.width = 1

    def __str__(self):
        return "{} {} {} {}".format(self.mnemonic, self.bytes, self.cycles, self.flags)

    def __repr__(self):
        return self.__str__()