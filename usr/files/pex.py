with open("pextest.pex", "r") as f:
    data = f.read()

lines = data.split("\n")

for i in lines:
    if i == "\n":
        i = ""

terms = []

for i in lines:
   terms.append(i.split(" ")) 

variables = {} 
functions = {}

ptr = 0

while ptr < len(terms):
    current = terms[ptr]

    if current[0] == "int":
        variables[current[1]] = int(current[3])
        ptr += 1
    elif current[0] == "flt":
        variables[current[1]] = float(current[3])
        ptr += 1
    elif current[0] == "str":
        variables[current[1]] = lines[ptr][lines[ptr].find("\"") + 1:-1]
        ptr += 1
    elif current[0] == "ch":
        variables[current[1]] = current[3][1]
        ptr += 1
    elif current[0] == "b":
        variables[current[1]] = current[3][2::]
        ptr += 1
    elif current[0] == "fn":
        functions[current[1]] = [ptr + 1, 0]
        while lines[ptr] != "}":
            ptr += 1
        ptr += 1

    elif current[0] == "if":
        comp_var1 = current[2]
        comp_var2 = current[4]

        if comp_var1 in variables:
            comp_var1 = variables[comp_var1]

        if comp_var2 in variables:
            comp_var2 = variables[comp_var2]

        if comp_var2[0] == "\"":
            comp_var2 = lines[ptr][lines[ptr].find("\"") + 1:-5]

        if type(comp_var1) == int or float:
            comp_var1 = float(comp_var1)

        if type(comp_var2) == int or float:
            comp_var2 = float(comp_var2)

        if current[3] == "==":
            if comp_var1 == comp_var2:
                ptr += 1
            else:
                while lines[ptr] != "}":
                    ptr += 1
                ptr += 1

        if current[3] == "!=":
            if comp_var1 != comp_var2:
                ptr += 1
            else:
                while lines[ptr] != "}":
                    ptr += 1
                ptr += 1

        if current[3] == ">":
            if float(comp_var1) > float(comp_var2):
                ptr += 1
            else:
                while lines[ptr] != "}":
                    ptr += 1
                ptr += 1

        # add < <= >= 

    elif current[0] == "print":
        txt = ""
        if current[2] in variables:
            txt = variables[current[2]]
        else:
            txt = lines[ptr][lines[ptr].find("(") + 2:lines[ptr].find(")") - 1]

        print(txt)
        ptr += 1

    elif current[0] in functions:
        functions[current[0]][1] = ptr + 1
        ptr = functions[current[0]][0]

    elif current[0] == "return":
        ptr = functions[current[1]][1]

    elif current[0] in variables:
        sec_val = ""

        if current[2] in variables:
            sec_val = variables[current[2]]
        else:
            sec_val = current[2]

        if type(sec_val) == int or float:
            sec_val = float(sec_val)

        if current[1] == "=":
            variables[current[0]] = sec_val
        elif current[1] == "+=":
            variables[current[0]] += sec_val
        elif current[1] == "-=":
            variables[current[0]] -= sec_val
        ptr += 1

    else:
        ptr += 1



