import sys
import re
from functools import reduce
import math

# Link: https://adventofcode.com/2024/day/1
# Solved: 11/30/2024

input = open(sys.argv[1]).read().strip()

# Problem summary:
# - P1: Get sum of distances of closest left-right pairs
#       (basically just sort and grab corresponding indexes)
# - P2: Every time a left value is in the rights list, sum that value.
#       The AoC description is verbose but basically just:
#       `for l in lefts, if l in rights. total += l`

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

# Get left andd right values
lines = input.split("\n")
lefts = []
rights = []
for line in lines:
    l, r = re.findall(r"(\d+)", line)
    lefts.append(l)
    rights.append(r)

# Sort lefts and rights
lefts.sort()
rights.sort()

# Get distance between each pair
dists = [abs(int(lefts[i]) - int( rights[i] )) for i in range(len(lefts))]

# P1 is sum of distances
p1 = sum(dists)

# For each left, add each time it is in the rights
total = 0
for l in lefts:
    for r in rights:
        if l == r:
            total += int(l)

# P2 is total
p2 = total

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)
