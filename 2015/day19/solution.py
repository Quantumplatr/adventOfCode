import sys
import re
from functools import reduce
import math

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

mapping_txt, molecule = input.split("\n\n")

mappings = {}

for line in mapping_txt.split("\n"):
    from_mol, to = re.findall(r"(\w+) => (\w+)", line)[0]
    
    if from_mol not in mappings:
        mappings[from_mol] = []
        
    mappings[from_mol].append(to)


def get_replacements(mol, mappings):
    parts = re.findall(r"[A-Z][a-z]?", mol)
    res = set()
    for i, m in enumerate(parts):
        
        if m not in mappings:
            continue
        
        reps = mappings[m]
        
        for rep in reps:
            replaced = parts[0:i] + [rep] + parts[i+1:]
            res.add("".join(replaced))
            
    return res

res = get_replacements(molecule, mappings)

        
p1 = len(res)

# P2 
# This is hard.
# TODO: come back to this and try again eventually
# (https://www.reddit.com/r/adventofcode/comments/3xflz8/day_19_solutions/)
# Key is that input uses Rn, Y, and Ar specially. 
# Treated as ( and , and ) respectively
# Can do math on counts or something

# starts = mappings["e"]

# def min_ignore_null(inputs):
#     min_so_far = None
#     for i in inputs:
        
#         if i is None:
#             continue
        
#         if min_so_far is None or i < min_so_far:
#             min_so_far = i
            
#     return min_so_far

# def get_min_steps(goal, curr, steps, mappings):
#     print(steps)
#     # Found!
#     if goal == curr:
#         return steps
    
#     # Try each replacement
#     reps = get_replacements(curr, mappings)
    
#     # print(f'From {curr}, {steps}: {" ".join([r for r in reps])}')
    
#     for next in sorted(reps, key=len):
#         if len(next) > len(goal):
#             continue
        
#         s = get_min_steps(goal, next, steps+1, mappings)
        
#         if s is not None:
#             return s
        
#     return None
    
# p2 = min_ignore_null([get_min_steps(molecule, start, 1, mappings) for start in mappings["e"]])

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)