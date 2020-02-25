from utils import TextInstruction
import os, json

mnemonic_map = {
    'ADC':'AddWithCarry',
    'ADD':'Add',
    'AND':'BinAnd',
    'BIT':None,
    'CALL':None,
    'CCF':None,
    'CP':'Compare',
    'CPL':None,
    'DAA':None,
    'DEC':'Decrement',
    'DI':None,
    'EI':None,
    'HALT':None,
    'INC':None,
    'INVALID':'InvalidInstruction',
    'JP':None,
    'JR':None,
    'LD':'Load',
    'LDH':'Load',
    'NOP':'NoOp',
    'OR':'BinOr',
    'POP':None,
    'PREFIX':'InvalidInstruction',
    'PUSH':None,
    'RES':'Reset',
    'RET':None,
    'RETI':None,
    'RL':'RotateLeft',
    'RLA':'RotateLeft',
    'RLC':'RotateLeftWithCarry',
    'RLCA':'RotateLeftWithCarry',
    'RR':'RotateRight',
    'RRA':'RotateRight',
    'RRC':'RotateRightWithCarry',
    'RRCA':'RotateRightWithCarry',
    'RST':None,
    'SBC':'SubtractWithCarry',
    'SCF':None,
    'SET':None,
    'SLA':None,
    'SRA':None,
    'SRL':None,
    'STOP':None,
    'SUB':'Subtract',
    'SWAP':None,
    'XOR':'BinXor',
}

immediate_operands = {'d8', 'd16', 'a8', 'a16', 'r8'}
register_operands = {'A', 'F', 'B', 'C', 'D', 'E', 'H', 'L', 'AF', 'BC', 'DE', 'HL', 'SP', 'PC'}

def translate_flags(instr):
    # for now
    return 'None'

def translate_operand(operand):
    if operand is None:
        return 'None'

    is_memory_access = '(' in operand and ')' in operand
    is_special_case = "SP" in operand and "+" in operand

    if operand in immediate_operands:
        # bit of a hack ;)
        byte_length = len(operand) - 1
        op_txt = "Operand.mem({})" if is_memory_access else "Operand.imm({})"
        return op_txt.format(byte_length)
    elif operand in register_operands:
        if is_special_case and not is_memory_access:
            # this is a pretty special operand that we'd rather deal with separately
            return "Operand.regI(SP)"

        # General case:
        op_txt = "Operand.regi({}, {})" if is_memory_access else "Operand.reg({}, {})"
        return op_txt.format(operand, len(operand))
#end

def translate_operands(instr):
    # Returns something like
    # "( Operand.reg(Registers.SP, 2), Operand.imm(2) )"
    # TODO: some single operand instructions act on themselves. Others act on the accumulator by definition.
    #       we need to be able to generate 2 operands here so it becomes unambiguous
    tokens = instr.mnemonic.split()
    if len(tokens) < 1:
        # No operands, just return None
        return 'None'
    else:
        src = dst = None
        if ',' in tokens:
            dst, src = tokens.split(',')
        else:
            # Unary instruction
            # TODO:this is where we need to check if destination is accumulator or the source!
            dst = src = tokens

        # now translate the operands
        dst_text = translate_operand(dst)
        src_text = translate_operand(src)
        return '( %s, %s )' % dst_text, src_text
    #end else
#end

def translate_mnemonic(instr):
    base = instr.mnemonic.split()[0]
    return mnemonic_map[base]
#end

def create_instruction(instr, file_handle):
    file_handle.write('    Instruction(\n')
    # TODO: parse bus_width from instruction source?
    file_handle.write('        {0:02X}, "{1}", bus_width=1,\n'.format(instr.opcode, instr.mnemonic))
    file_handle.write('        byte_size={}, cycles={},\n'.format(instr.bytes, instr.cycles))
    file_handle.write('        flags={},\n'.format(translate_flags(instr)))
    file_handle.write('        operands = {},\n'.format(translate_operands(instr)))
    file_handle.write('        executor = {}),\n'.format(translate_mnemonic(instr)))
    file_handle.flush()
#end create

def generate_instructions(instruction_list, given_name, file_handle):
    file_handle.write('{} = [\n'.format(given_name))
    for instruction in instruction_list:
        create_instruction(instruction, file_handle)
    #end for
    file_handle.write(']'.format(given_name))
#end generate

def read_and_generate(filename, list_name, file_handle):
    instruction_list = None
    with open(filename, 'r') as instructions:
        instruction_list = [x.rstrip().lstrip() for x in instructions.readlines()]
    generate_instructions(instruction_list, list_name, file_handle)
#end read_and_generate

def create_header(file_handle):
    file_handle.write('from .cpu_types import *\n')
    file_handle.write('from .instructions import *\n')
    file_handle.write('\n')
    file_handle.write('# The list below is every single opcode that we know is needed for emulating Game Boy\n')
    file_handle.write('# Most of the info below was compiled from the very useful opcode sheet below\n')
    file_handle.write('#  https://www.pastraiser.com/cpu/gameboy/gameboy_opcodes.html\n')
    file_handle.write('# Trying to read through this list is rather impossible, so searching by opcode or mnemonic is your best bet.\n')
    file_handle.write('\n')
#end create_header

def main():
    with open('../src/known_instructions.py', 'w') as target_file:
        create_header(target_file)
        read_and_generate('./gb_base.json', 'base_instructions', target_file)
        read_and_generate('./gb_cb_prefix.json', 'cb_prefix', target_file)
    #close target_file
#end

if __name__ == "__main__":
    main()