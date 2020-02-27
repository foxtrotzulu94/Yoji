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
    'INC':'Increment',
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
    'SBC':'SubWithCarry',
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

flag_operands = { 'NZ', 'Z', 'NC', 'C' }
immediate_operands = {'d8', 'd16', 'a8', 'a16', 'r8'}
register_operands = {'A', 'F', 'B', 'C', 'D', 'E', 'H', 'L', 'AF', 'BC', 'DE', 'HL', 'SP', 'PC'}
unary_map = {
    'AND': 'A',
    'OR': 'A',
    'XOR': 'A',
    'RRA': 'A',
    'RRCA': 'A',
    'RLA': 'A',
    'RLCA': 'A',
}

def translate_flags(instr):
    if instr.flags is None:
        return 'None'

    if all(x == '-' for x in instr.flags):
        # No flags are affected
        return 'None'

    flags = { 'Flag.z':instr.flags[0], 'Flag.n':instr.flags[1], 'Flag.h':instr.flags[2], 'Flag.c':instr.flags[3] }
    translation = []
    for bit, val in flags.items():
        actual_val = 'Bit.Calculate'
        if val == '-':
            actual_val = 'Bit.Ignore'
        elif val.isdigit():
            actual_val = 'Bit.Set' if val == '1' else 'Bit.Reset'

        translation.append("{}:{}".format(bit, actual_val))

    flag_string= "{ %s }" % ", ".join(translation)
    return flag_string
#end

def translate_operand(operand):
    if operand is None:
        return 'None'

    is_memory_access = '(' in operand and ')' in operand
    is_special_case = "SP" in operand and "+" in operand and not is_memory_access
    is_post_increment = is_memory_access and "+" in operand
    is_post_decrement = is_memory_access and "-" in operand
    is_constant = (operand.isdigit() and len(operand) == 1) or (operand.endswith('H') and len(operand) == 3)

    # strip characters out
    remove_map = str.maketrans({x:None for x in '()+-'})
    operand = operand.translate(remove_map)

    if is_constant:
        # Hex constants like 00H
        if operand.endswith('H'):
            operand = operand[:-1]
            return "Operand.const(0x{})".format(operand)

        # Bit constant, which are just digits
        return "Operand.const({})".format(operand)
    elif operand in immediate_operands:
        # bit of a hack ;)
        byte_length = len(operand) - 1
        op_txt = "Operand.mem({})" if is_memory_access else "Operand.imm({})"
        return op_txt.format(byte_length)
    elif operand in register_operands:
        # General case: Register Addressing
        op_txt = "Operand.reg(Registers.{}, {})"
        if is_post_increment:
            op_txt = "Operand.regInc(Registers.{}, {})"
        elif is_post_decrement:
            op_txt = "Operand.regDec(Registers.{}, {})"
        elif is_memory_access:
            op_txt = "Operand.regi(Registers.{}, {})"
        return op_txt.format(operand, len(operand))
    elif operand in flag_operands:
        bit = operand[-1].lower()
        state = "Bit.Set" if len(operand) == 1 else "Bit.Reset"
        return "Operand.bit(Flag.{}, {})".format(bit, state)
    elif is_special_case:
        # this is a pretty special operand that I'd rather deal with as a one-off
        return "Operand.regI(Registers.SP)"
    elif operand == 'CB':
        return None

    raise NotImplementedError("Operand {} is not implemented!".format(operand))
#end

def translate_operands(instr):
    # Returns something like
    # "( Operand.reg(Registers.SP, 2), Operand.imm(2) )"
    # TODO: some single operand instructions act on themselves. Others act on the accumulator by definition.
    #       we need to be able to generate 2 operands here so it becomes unambiguous
    tokens = instr.mnemonic.split()
    if len(tokens) < 2:
        # No operands, just return None
        return 'None'
    else:
        op_tks = tokens[1]
        src = dst = None
        if ',' in op_tks:
            dst, src = op_tks.split(',')
        else:
            # Unary instruction
            # TODO:this is where we need to check if destination is accumulator or the source!
            dst = src = op_tks

        # now translate the operands
        dst_text = translate_operand(dst)
        src_text = translate_operand(src)

        if dst_text == 'None' and src_text == dst_text:
            return 'None'

        return '( {}, {} )'.format(dst_text, src_text)
    #end else
#end

def translate_mnemonic(instr):
    base = instr.mnemonic.split()[0]
    return mnemonic_map[base]
#end

def create_instruction(instr, file_handle):
    file_handle.write('    Instruction(\n')
    # TODO: parse bus_width from instruction source?
    file_handle.write('        0x{0:02X}, "{1}", bus_width={2},\n'.format(instr.opcode, instr.mnemonic, instr.width))
    file_handle.write('        byte_size={}, cycles={},\n'.format(instr.bytes, instr.cycles))
    file_handle.write('        flags={},\n'.format(translate_flags(instr)))
    file_handle.write('        operands = {},\n'.format(translate_operands(instr)))
    file_handle.write('        executor = {}),\n'.format(translate_mnemonic(instr)))
    file_handle.write('        \n')
    file_handle.flush()
#end create

def generate_instructions(instruction_list, given_name, file_handle):
    file_handle.write('{} = [\n'.format(given_name))
    for instruction in instruction_list:
        create_instruction(instruction, file_handle)
    #end for
    file_handle.write(']\n\n'.format(given_name))
#end generate

def read_and_generate(filename, list_name, file_handle):
    import json
    instruction_list = None
    with open(filename, 'r') as instructions:
        data = json.load(instructions)
        instruction_list = [TextInstruction.from_json(x) for x in data]
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
    file_handle.flush()
#end create_header

def main():
    out_filename = '../src/known_instructions.py'
    if os.path.exists(out_filename):
        os.remove(out_filename)

    with open('../src/known_instructions.py', 'w') as target_file:
        create_header(target_file)
        read_and_generate('./gb_base.json', 'known_instructions', target_file)
        read_and_generate('./gb_cb_prefix.json', 'cb_prefix', target_file)
    #close target_file
#end

if __name__ == "__main__":
    main()