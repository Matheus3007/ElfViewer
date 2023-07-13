import re
import csv
from typeChooser import typeChooser

def parse_objdump(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    
    instruction_pattern = re.compile(r'\s*([0-9a-f]+):\s*([0-9a-f]+)\s*(\S+).*')

    instructions = []
    index = 0
    # gets first line address
    first_line = lines[0]
    match = instruction_pattern.match(first_line)

    for line in lines:
        match = instruction_pattern.match(line)
        if match:
            address, value, instruction = match.groups()
            starting_address = int(address, 16)
            break


    

    for line in lines:

        match = instruction_pattern.match(line)
        if match:
            address, value, instruction = match.groups()
           # value = int(value, 16)
            identifier_value = format(int(value[1], 16), '04b')
            whole_instruction = format(int(value, 16), '032b')
            group = typeChooser(whole_instruction)
            memory_index = int(((int(address, 16) - starting_address))/4)
            if instruction == "msr":
                group = "COPROCESSOR"
            if instruction == "mrs":
                group = "COPROCESSOR"
            if group == "UNDEFINED" and instruction == "ldr" or instruction == "str":
                group = "LOAD STORE"
            instructions.append({
                'index': index,
                'memory_index': memory_index,
                'address': address,
                'instruction': instruction,
                'value': value,
                'whole_binary': whole_instruction,
                'group': group,
                'type': identifier_value
            })
            index += 1

    return instructions

'''
def get_unique_values(data, key):
    values = set(item[key] for item in data)
    return list(values)

uniqueVals = get_unique_values(instructions, 'instruction')


with open("instrucoes.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for item in uniqueVals:
        writer.writerow([item])


instructions = parse_objdump('objdump.txt')
for i in instructions[0:100]:
#    print(i['index'])
    print("instruction index (virtual adress): " + str(i['index'])+ " memory index: " + str(i['memory_index']))
    print(i['instruction'])
    print(i['group'])
    
#    print(i['whole_binary'][-28]+i['whole_binary'][-27]+i['whole_binary'][-26])
#    print(i['whole_binary'][-25]+i['whole_binary'][-24])
    print("------------------")
    '''