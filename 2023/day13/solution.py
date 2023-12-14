import sys
import re
from functools import reduce
import math

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

# Check for vert mirror
patterns = input.split("\n\n")

def transpose(pattern):
    lines = pattern.split("\n")
    chars = [[c for c in line] for line in lines]
    t = list(map(list, zip(*chars))) # https://stackoverflow.com/questions/6473679/transpose-list-of-lists
    new_lines = ["".join(line) for line in t]
    new_pat = "\n".join(new_lines)
    
    return new_pat 

def get_row_bef_mir(pattern):
    lines = pattern.split("\n")
    for row, line in enumerate(lines):
        half = len(lines) / 2
        if row > half:
            rem = len(lines) - row
            if lines[row-rem:row] == (lines[row:])[::-1]:
                return row
            
        elif row > 0:
            if lines[:row] == (lines[row:2*(row)])[::-1]:
                return row
            
    return None

def get_row_w_smudge(pattern):
    lines = pattern.split("\n")
    for row, line in enumerate(lines, 1):
        half = len(lines) / 2
        
        lines1 = None
        lines2 = None
        if row > half:
            rem = len(lines) - row
            lines1 = lines[row-rem:row]
            lines2 = (lines[row:])[::-1]
            
        else:
            lines1 = lines[:row]
            lines2 = (lines[row:2*(row)])[::-1]
                
                
        # Count diffs
        diffs = 0
        for i, l1 in enumerate(lines1):
            for j, c1 in enumerate(l1):
                c2 = lines2[i][j]
                
                if c1 != c2:
                    diffs += 1
                    
        if diffs == 1:
            return row
            
    return None

for pattern in patterns:
    row = get_row_bef_mir(pattern)
    t = transpose(pattern)
    col = get_row_bef_mir(t)
    
    if row is not None:
        p1 += row * 100
        
    if col is not None:
        p1 += col
        
        
            

for pattern in patterns:
    row = get_row_w_smudge(pattern)
    t = transpose(pattern)
    col = get_row_w_smudge(t)
    
    if row is not None:
        p2 += row * 100
        
    if col is not None:
        p2 += col

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)