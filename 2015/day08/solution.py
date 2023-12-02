import sys
from functools import reduce

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

def get_counts(lines) -> (int, int):
    
    total_code = 0
    total_mem = 0

    for line in lines:
        
        code_count = 0
        mem_count = 0
        
        i = 0
        while i < len(line):
            
            if i == 0 or i == len(line) - 1:
                code_count += 1
                i += 1
                continue
            
            if line[i] == "\\":
                if line[i+1] == 'x':
                    i += 4
                    code_count += 4
                    mem_count += 1
                    continue
                else:
                    i += 2
                    code_count += 2
                    mem_count += 1
                    continue
                
            code_count += 1
            mem_count += 1
            i += 1
        
        total_code += code_count
        total_mem += mem_count
        
    return (total_code, total_mem)

def encode_line(line):
    new_line = ""
    
    for char in line:
        if char in ["\\", "\""]:
            new_line += "\\"
        new_line += char
    
    return "\"" + new_line + "\""
            
lines = input.split("\n")
total_code1, total_mem1 = get_counts(lines)
total_code2, total_mem2 = get_counts([encode_line(line) for line in lines])

p1 = total_code1 - total_mem1
p2 = total_code2 - total_code1


# ------------------- #

print(p1, p2)