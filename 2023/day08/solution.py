import sys
import re
from functools import reduce
import math

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

header, data = input.split("\n\n")

mappings = {}

for line in data.split("\n"):
    places = re.findall(r"(\w+)\s=\s\((\w+),\s(\w+)\)", line)[0]

    fro, left, right = places

    mappings[fro] = (left, right)

# P1

i = 0
pos = "AAA"
steps = 0
while pos != "ZZZ":
    steps += 1

    ind = 0 if header[i] == "L" else 1

    pos = mappings[pos][ind]

    # Inc or loop
    i += 1
    if i >= len(header):
        i = 0

p1 = steps

# P2

positions = [key for key, val in mappings.items() if key[-1] == "A"]
i = 0
steps = 0

def find_next_z(mappings, from_pos, header, from_ind) -> (str, int, int):
    i = from_ind
    steps = 0
    curr = from_pos
    
    # If already ends with Z, move once
    if curr[-1] == "Z":
        steps += 1
        
        ind = 0 if header[i] == "L" else 1
        curr = mappings[curr][ind]

        # Inc or loop
        i += 1
        if i >= len(header):
            i = 0
    
    
    while curr[-1] != "Z":
        steps += 1
        ind = 0 if header[i] == "L" else 1
        curr = mappings[curr][ind]

        # Inc or loop
        i += 1
        if i >= len(header):
            i = 0

    return (curr, steps, i)

step_counts = []
for pos in positions:
    
    curr = pos
    
    steps = 0
    i = 0
    while curr[-1] != "Z":
        steps += 1
        
        ind = 0 if header[i] == "L" else 1
        
        last = curr
        curr = mappings[curr][ind]
        
        # Inc or loop
        i += 1
        if i >= len(header):
            i = 0
    
    step_counts.append(steps)
    
p2 = math.lcm(*step_counts)
    

# --- Trying to figure out why this works --- # 

# def is_in_loop(loop, curr):
#     # Curr: (position, steps, index in header)
#     # Curr is in loop if loop has item with same position and index
    
#     curr_p, curr_s, curr_i = curr
    
#     for p, s, i in loop:
#         if p == curr_p and i == curr_i:
#             return True
        
#     return False
    
# loops = {}

# for pos in positions:
#     print(pos)
#     curr = pos
    
#     loops[pos] = [(pos, 0, 0)]
    
#     steps = 0
#     i = 0
    
#     while not is_in_loop(loops[pos][:-1], loops[pos][-1]) or steps == 0:
#         # print(steps)
        
#         steps += 1
        
#         ind = 0 if header[i] == "L" else 1
#         curr = mappings[curr][ind]
#         loops[pos].append((curr, steps, i))
#         # print((curr, steps, i))
        
#         # Inc or loop
#         i += 1
#         if i >= len(header):
#             i = 0
    
# print('h')
# for start, loop in loops.items():
    
#     # num z
#     num_z = 0
#     for part in loop:
#         p, s, ind = part
#         if p[-1] == "Z":
#             num_z += 1
    
#     print(start, num_z, len(loop), loop)
    



# ------------------- #

print(p1, p2)
