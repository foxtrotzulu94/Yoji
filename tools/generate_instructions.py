from utils import TextInstruction
import os, json

mnemonic_map = {
    'ADC':'AddWithCarry',
    'ADD':'Add',
    'AND':'BinAnd',
    'BIT':'CheckBit',
    'CALL':'Call',
    'CCF':'InvertCarry',
    'CP':'Compare',
    'CPL':'ComplementA',
    'DAA':'DecimalAdjustAccumulator',
    'DEC':'Decrement',
    'DI':'DisableInterrupts',
    'EI':'EnableInterrupts',
    'HALT':'Halt',
    'INC':'Increment',
    'INVALID':'InvalidInstruction',
    'JP':'Jump',
    'JR':'NearJump',
    'LD':'Load',
    'LDH':'Load',
    'NOP':'NoOp',
    'OR':'BinOr',
    'POP':'Pop',
    'PREFIX':'InvalidInstruction',
    'PUSH':'Push',
    'RES':'Reset',
    'RET':'Return',
    'RETI':'ReturnInterrupt',
    'RL':'RotateLeft',
    'RLA':'RotateLeft',
    'RLC':'RotateLeftWithCarry',
    'RLCA':'RotateLeftWithCarry',
    'RR':'RotateRight',
    'RRA':'RotateRight',
    'RRC':'RotateRightWithCarry',
    'RRCA':'RotateRightWithCarry',
    'RST':'Restart',
    'SBC':'SubWithCarry',
    'SCF':'SetCarry',
    'SET':'SetBit',
    'SLA':'ShiftLeft',
    'SRA':'ShiftRightArithmetic',
    'SRL':'ShiftRight',
    'STOP':'Stop',
    'SUB':'Subtract',
    'SWAP':'Swap',
    'XOR':'BinXor',
}

# Key is instructions, Value is writeback register
# When value is 'None', Writeback scenario is not supported
# When key==value, writeback to location
unary_instructions = {
    'ADC': 'A',
    'ADD': 'A',
    'AND': 'A',
    'CALL': None,
    'CP': None, # this is a bit of a lie, we write that it has a first operand but throwaway the result
    'DEC': 'DEC',
    'INC': 'INC',
    'JP': None,
    'JR': None,
    'OR': 'A',
    'POP': 'POP',
    'PREFIX': None,
    'PUSH': None,
    'RET': None,
    'RL': 'RL',
    'RLA': 'A',
    'RLC': 'RLC',
    'RLCA': 'A',
    'RR': 'RR',
    'RRA': 'A',
    'RRCA': 'A',
    'RRC': 'RRC',
    'RST': None,
    'SBC': 'SBC',
    'SLA': 'SLA',
    'SRA': 'SRA',
    'SRL': 'SRL',
    'SUB': 'A',
    'SWAP': 'SWAP',
    'XOR': 'A',
}

flag_operands = { 'NZ', 'Z', 'NC', 'C' }
immediate_operands = {'d8', 'd16', 'a8', 'a16', 'r8'}
register_operands = {'A', 'F', 'B', 'C', 'D', 'E', 'H', 'L', 'AF', 'BC', 'DE', 'HL', 'SP', 'PC'}

swap_operands = {'SET'}

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
        return 'None'

    raise NotImplementedError("Operand {} is not implemented!".format(operand))
#end

def translate_operands(instr):
    # Returns something like
    # "( Operand.reg(Registers.SP, 2), Operand.imm(2) )"

    tokens = instr.mnemonic.split()
    base = tokens[0]
    dst = src = None
    if len(tokens) < 2:
        if not base in unary_instructions or unary_instructions[base] is None:
            # No operands, just return None
            return 'None'

        # Operand is both source and destination
        src = dst = unary_instructions[base]

    else:
        op_tks = tokens[1]
        if ',' in op_tks:
            dst, src = op_tks.split(',')
        else:
            # Unary instruction
            assert(base in unary_instructions)

            # Special case, compare instruction
            if base == 'CP':
                return "( Operand.reg(Registers.A, throwaway = True), {} )".format(translate_operand(op_tks))

            writeback_reg = unary_instructions[base]
            if writeback_reg == base:
                dst = src = op_tks
            else:
                dst = writeback_reg
                src = op_tks
    #end if-else on tokens

    # now translate the operands
    dst_text = translate_operand(dst)
    src_text = translate_operand(src)

    if dst_text == 'None' and src_text == dst_text:
        return 'None'

    if base in swap_operands:
        # A bit of a hack so we can have writeback
        src_text, dst_text = dst_text, src_text


    return '( {}, {} )'.format(dst_text, src_text)
    #end else
#end

def translate_mnemonic(instr):
    base = instr.mnemonic.split()[0]
    return mnemonic_map[base]
#end

def unpack_cycles(cycle_text):
    if type(cycle_text) is not str:
        return cycle_text

    parts = cycle_text.split('/')
    if len(parts) == 1:
        return cycle_text
    
    return "({},{})".format(*parts)

def create_instruction(instr, file_handle):
    file_handle.write('    Instruction(\n')
    # TODO: parse bus_width from instruction source?
    file_handle.write('        0x{0:02X}, "{1}", bus_width={2},\n'.format(instr.opcode, instr.mnemonic, instr.width))
    file_handle.write('        byte_size={}, cycles={},\n'.format(instr.bytes, unpack_cycles(instr.cycles)))
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

def read_instruction_data(filename):
    result = None
    with open(filename, 'r') as a_file:
        data = json.load(a_file)
        result = [TextInstruction.from_json(x) for x in data]
    return result
#end

def read_and_generate(filename, list_name, file_handle):
    import json
    instruction_list = read_instruction_data(filename)
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
    known_filenames = ['../src/known_instructions.py', '../src/base_instructions.py', '../src/cb_prefix_instructions.py']
    for out_filename in known_filenames:
        if os.path.exists(out_filename):
            os.remove(out_filename)

    with open('../src/base_instructions.py', 'w') as base_file:
        create_header(base_file)
        read_and_generate('./gb_base.json', 'base_instructions', base_file)
    #close file

    with open('../src/cb_prefix_instructions.py', 'w') as cb_file:
        create_header(cb_file)
        read_and_generate('./gb_cb_prefix.json', 'cb_prefix', cb_file)
    #close file
#end

if __name__ == "__main__":
    main()