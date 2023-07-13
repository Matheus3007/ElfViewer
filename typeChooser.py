def typeChooser(instruction):
    if instruction[-28] == "0": # 0__
        if instruction[-27] == "0": # 00_
            if instruction[-26] == "0": # 000
                ## bits 11 to 7 must equal 00001 as to be a load store half word instruction
                if instruction[-12:-8] == "00001":
                    return "Load Store Half Word"
                ## if bits 16 to 12 equal 1, its an msr or mrs instruction
                elif instruction[-17:-13] == "11111":
                    return "msr"
                ## if bits 19 to 16 equal 1, its mrs instruction
                elif instruction[-20:-17] == "1111":
                    return "mrs"
                else:
                    return "BRANCH"
                    pri
                print("testar shift/branch")
            else: # 001
                return "ALU"
        else: # 01_
            if instruction[-26] == "0": # 010
                return "UNDEFINED"
                print("NADA")
            else: # 011
                return "LOAD STORE INDEXED"
                print("Load Store com registrador de indice")
                
    else: # 1__
        if instruction[-27] == "0": # 10_
            if instruction[-26] == "0": # 100
                return "LOAD STORE MULTIPLE"
                print("Load Store Multiple")
            else: # 101
                return "BRANCH"
                print("Salto")
        else: # 11_
            if instruction[-26] == "0": # 110
                return "COPROCESSOR"
                print("Load store coprocessador")
            else: # 111
                return "COPROCESSOR"
                print("Move coprocessador")
            
