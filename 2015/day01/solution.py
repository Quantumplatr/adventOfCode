import sys
from functools import reduce

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

floor = 0
first_basement = -1
for i, char in enumerate(input):
    floor += 1 * (1 if char == "(" else -1)
    
    if floor == -1 and first_basement == -1:
        first_basement = i + 1
    
p1 = floor
p2 = first_basement

# ------------------- #

print(p1, p2)