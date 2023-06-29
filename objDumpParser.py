import re

def parse_objdump(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    instruction_pattern = re.compile(r'\s*([0-9a-f]+):\s*([0-9a-f]+)\s*(\S+).*')

    instructions = []

    for line in lines:
        match = instruction_pattern.match(line)
        if match:
            address, value, instruction = match.groups()
            instructions.append({
                'address': address,
                'instruction': instruction,
                'value': value
            })

    return instructions

instructions = parse_objdump('objdump.txt')