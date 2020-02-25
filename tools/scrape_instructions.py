from html.parser import HTMLParser

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

class HTMLOpcodesInstructions(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = []
        self.curr_inst = None
        self.parsing_td = False
        self.step = 0

    def handle_starttag(self, tag, attrs):
        if tag=='td':
            self.parsing_td = True
            assert(self.curr_inst is None)
            self.curr_inst = TextInstruction(len(self.data))

    def handle_endtag(self, tag):
        if(tag=='td'):
            assert(self.parsing_td)
            self.data.append(self.curr_inst if self.curr_inst.bytes != -1 else TextInstruction(self.curr_inst.opcode))
            self.curr_inst = None
            self.parsing_td = False
            self.step = 0

    def handle_data(self, data):
        if self.parsing_td:
            if self.step == 0:
                self.curr_inst.mnemonic = data
            elif self.step == 1:
                self.curr_inst.bytes, self.curr_inst.cycles = data.split()
            elif self.step == 2:
                self.curr_inst.flags = data.split()

            self.step += 1
        #end if
#end

def open_and_parse(filename, result_filename):
    import json, os
    parser = HTMLOpcodesInstructions()
    with open(filename, 'r') as html_file:
        parser.feed(html_file.read())
    #end

    if os.path.exists(result_filename):
        os.remove(result_filename)
    with open(result_filename, 'w') as result_file:
        json.dump(parser.data, result_file, indent=4, cls=TextInstruction.Serializer)

def main():
    open_and_parse('./gb_256_base.html', 'gb_base.json')
    open_and_parse('./gb_256_cb_prefix.html', 'gb_cb_prefix.json')

if __name__ == "__main__":
    main()