import sys
import re
from functools import reduce
import math
import pyperclip

# Solved: 12/3/2024
# Things to improve:
# - Today felt messy
# - I'm not sure immediately how I could've improved beyond just figuring it out quicker
# - My traversal felt pretty messy.
# - Not sure the best way to do the directional checks quicker
# - Lots of little things I could've done I think. Idk

input = open(sys.argv[1]).read().strip()

p1 = 0
p2 = 0

# ---- CODE HERE ---- #

lines = input.split("\n")

# True if coords are in bounds of `lines`
def in_bounds(i, j):
    h = len(lines)
    w = len(lines[0])
    return i >= 0 and i < h and j >= 0 and j < w

# Count the number of "MAS"s going away from the assumed "X" at (i,j)
def xmas_count(i,j) -> int:
    count = 0
    dirs = [
        (1,0), # E
        (-1,0), # W
        (0,1), # S
        (0, -1), # N
        (1,1), # SE
        (-1,1), # SW
        (1,-1), # NE
        (-1,-1), # NW
    ]

    # Go through each dir
    for dir in dirs:
        # If whole word would be in bounds:
        if in_bounds(i+3*dir[0],j+3*dir[1]):
            # NOTE: Probably could've done this a lot cleaner. Idk
            m = lines[i+dir[0]][j+dir[1]] # First letter
            a = lines[i+2*dir[0]][j+2*dir[1]] # Second letter
            s = lines[i+3*dir[0]][j+3*dir[1]] # Third letter

            # Check if letters are correct
            if m == "M" and a == "A" and s == "S":
                count += 1
    return count

# True if diagonals spell "MAS" with "A" assumedly at (i,j)
def is_x_mas(i,j) -> bool:
    points = [
        (-1, -1),
        (1, 1),
        (1, -1),
        (-1, 1),
    ]

    # Make sure corners in bounds
    for point in points:
        if not in_bounds(i+point[0],j+point[1]):
            return False

    # Get corner values
    tl = lines[i-1][j-1]
    tr = lines[i-1][j+1]
    bl = lines[i+1][j-1]
    br = lines[i+1][j+1]

    # Check corner vals
    # NOTE: this was messy. could've done much better
    d1 = False
    if tl == "S":
        if br == "M":
             d1 = True
    elif tl == "M":
        if br == "S":
             d1 = True

    d2 = False
    if tr == "S":
        if bl == "M":
            d2 = True
    elif tr == "M":
        if bl == "S":
            d2 = True

    return d1 and d2

# Traverse grid of letters
for i in range(len(lines)):
    for j in range( len(lines[i]) ):
        char = lines[i][j]
        # If at "X", check for "XMAS"s
        if char == "X":
            p1 += xmas_count(i,j)

        # If at "A", check for "MAS" on diagonals
        if char == "A":
            p2 += 1 if is_x_mas(i,j) else 0

# ------------------- #

print("Part 1:", p1)
print("Part 2:", p2)

to_copy = p1 if p2 == 0 else p2
pyperclip.copy(to_copy)
print(f"Copied {'P1' if p2 == 0 else 'P2'}: \"{to_copy}\"")
