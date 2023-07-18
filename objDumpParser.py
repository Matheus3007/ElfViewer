import re
import csv
from tqdm import tqdm
from typeChooser import typeChooser

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
            if instruction == "msr":
                group = "COPROCESSOR"
            if instruction == "mrs":
                group = "COPROCESSOR"
            if group == "UNDEFINED" and instruction[:3] == "ldr" or instruction[:3] == "str":
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
    return instructions