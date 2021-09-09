from utils import TextInstruction, RefinedInstruction
from functools import reduce
import os, json

def main():
    base_instructions = None
    with open('gb_base.json', 'r') as base_file:
        base_instructions = json.load(base_file)
    #close file
    base_instructions = [TextInstruction.from_json(x) for x in base_instructions]

    cb_prefix_instructions = None
    with open('gb_cb_prefix.json', 'r') as cb_file:
        cb_prefix_instructions = json.load(cb_file)
    #close file
    cb_prefix_instructions = [TextInstruction.from_json(x) for x in cb_prefix_instructions]

    refined_instruction = [RefinedInstruction(instr) for instr in base_instructions]
    refined_instruction = refined_instruction + [RefinedInstruction(cb, 0xCB) for cb in cb_prefix_instructions]

    with open('gameboy_instructions.json', 'w') as data_file:
        json.dump(refined_instruction, data_file, indent=4, cls=RefinedInstruction.Serializer)
    #close

    operands_mesh = [x.operands for x in refined_instruction]
    operands_list = list(set(reduce(lambda x,y: x+y , operands_mesh) ))
    operands_list.sort()
    print(operands_list)
#end

if __name__ == "__main__":
    main()