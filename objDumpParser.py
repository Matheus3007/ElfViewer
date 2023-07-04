import re
import csv

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

def get_unique_values(data, key):
    values = set(item[key] for item in data)
    return list(values)

uniqueVals = get_unique_values(instructions, 'instruction')

with open("instrucoes.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for item in uniqueVals:
        writer.writerow([item])