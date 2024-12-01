import sys
import re
from functools import reduce
import math

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

lines = input.split("\n")

all_cals = []
i = 0
while i < len(lines):
    line = lines[i]
    cals = 0

    # For each group
    while line != "":
        cals += int(line)
        i += 1
        if i < len(lines):
            line = lines[i]
        else:
            break

    all_cals.append(cals)
    i += 1

all_cals.sort()
p1 = all_cals[-1]
p2 = sum(all_cals[-3:])

# Things I could've done better:
# - Split on "\n\n" to get groups immediately
#   This makes looping super easy

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)
