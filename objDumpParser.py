import re
import csv
from tqdm import tqdm
from typeChooser import typeChooser
alu_mnemonic_list = ["and", "eor", "sub", "rsb", "add", "adc", "sbc", "rsc", "tst", "teq", "cmp", "cmn", "orr", "mov", "bic", "mvn", "mul"]
stack_mnemonic_list = ["push", "pop"]
shift_list = ["lsl", "lsr", "asr", "ror", "rrx"]
coprocessor_list = ["cdp", "mcr", "mrc", "ldc", "stc", "mrs", "msr"]
def parse_objdump(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    
    instruction_pattern = re.compile(r'\s*([0-9a-f]+):\s*([0-9a-f]+)\s*(\S+).*')

    instructions = []
    index = 0

    # gets first address
    first_line = lines[0]
    match = instruction_pattern.match(first_line)
    for line in lines:
        match = instruction_pattern.match(line)
        if match:
            address, value, instruction = match.groups()
            starting_address = int(address, 16)
            print("First address acquired: " + str(starting_address) + "\n")
            break

    # builds dict and parses whole files
    for line in tqdm(lines, desc='Building dict', unit='line'):
        match = instruction_pattern.match(line)
        if match:
            address, value, instruction = match.groups()
            identifier_value = format(int(value[1], 16), '04b')
            whole_instruction = format(int(value, 16), '032b')
            group = typeChooser(whole_instruction)
            memory_index = int(((int(address, 16) - starting_address))/4)
            if group == "BRANCH" and instruction[:1] != "b":
                group = "UNDEFINED"
            if instruction == "msr":
                group = "COPROCESSOR"
            if instruction == "mrs":
                group = "COPROCESSOR"
            if group == "UNDEFINED" and (instruction[:3] in alu_mnemonic_list):
                group = "ALU"
            if group == "UNDEFINED" and (instruction[:4] in stack_mnemonic_list):
                group = "STACK"
            if group == "UNDEFINED" and (instruction[:3] in shift_list):
                group = "ALU"
            if group == "UNDEFINED" and (instruction[:3] in coprocessor_list):
                group = "COPROCESSOR"
            if group == "UNDEFINED" and (instruction[:2] == "ld" or instruction[:2] == "st"):
                group = "LOAD STORE"
            instructions.append({
                'index': index,                         # General dict index
                'memory_index': memory_index,           # Memory index, relative to the processor's memory
                'address': address,                     # Instruction address in hex
                'instruction': instruction,             # Instruction mnemonic
                'value': value,                         # Instruction value in hex
                'whole_binary': whole_instruction,      # Instruction value in binary
                'group': group,                         # General instruction macro group
            })
            index += 1
    print("Done!\n")
    filtered_instructions = [item for item in instructions if item.get("instruction") != ";"]
    return filtered_instructions