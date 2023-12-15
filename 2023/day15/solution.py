import sys
import re
from functools import reduce
import math

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

# Hash alg
def hash(s: str) -> int:
    h = 0
    
    for c in s:
        h += ord(c)
        h *= 17
        h = h % 256
    
    return h

# Sum hashes
for s in input.split(","):
    p1 += hash(s)
    
# P2

boxes = {}

# Put everything into hashmap
for s in input.split(","):
    text, oper = re.findall("(\w+)(.*)", s)[0]
    
    h = hash(text)
    
    # Remove if "-"
    if oper == "-":
        if h in boxes and text in boxes[h]:
            del boxes[h][text]
            
    # Add N if "=N"
    # N is focal length
    else:
        if h not in boxes:
            boxes[h] = {}
        boxes[h][text] = oper[1:]
        
# Calculate focus power
for box_num, box in boxes.items():
    num_in_box = 1
    for text, focus in box.items():
        # Power += product of:
        #  - The box number + 1
        #  - The slot within the box (1 based)
        #  - Focal length
        p2 += (box_num + 1) * num_in_box * int(focus)
        num_in_box += 1

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)