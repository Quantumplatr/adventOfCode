import sys
import re
from functools import reduce
import math

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

# universe = ""
universe = input

empty_rows = set()
empty_cols = set()

# Count empty rows
for i, row in enumerate(input.split("\n")):
    if len(set(row)) == 1:
        empty_rows.add(i)
        
# Count empty cols
for j in range(len(row)):
    col = [r[j] for r in input.split("\n")]
    if len(set(col)) == 1:
        empty_cols.add(j)
    
    
# Find galaxies
galaxies = []
for row, line in enumerate(universe.split("\n")):
    for col, char in enumerate(line):
        if char == "#":
            galaxies.append((row,col))
    
# Calculate sum of dists
for i in range(len(galaxies)):
    for j in range(i+1, len(galaxies)):
        # Get locations
        r1, c1 = galaxies[i]
        r2, c2 = galaxies[j]
        
        # Get distances
        dist1 = abs(r2 - r1) + abs(c2 - c1)
        dist2 = abs(r2 - r1) + abs(c2 - c1)
        
        # Add extra dist based on expansion of empty rows/cols
        scale1 = 2
        scale2 = 1_000_000
        for r in empty_rows:
            if r1 < r < r2 or r2 < r < r1:
                dist1 += scale1 - 1 # -1 b/c it's already counted once
                dist2 += scale2 - 1 # -1 b/c it's already counted once
        for c in empty_cols:
            if c1 < c < c2 or c2 < c < c1:
                dist1 += scale1 - 1 # -1 b/c it's already counted once
                dist2 += scale2 - 1 # -1 b/c it's already counted once
        
        # Generate sum
        p1 += dist1
        p2 += dist2

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)